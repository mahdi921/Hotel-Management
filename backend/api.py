"""
FastAPI Application - Hotel Management System API
Integrated with Django ORM for data access.

This module provides REST API endpoints for:
- Room availability and management
- Guest operations
- Booking with date overlap validation
- "Best Room" algorithm for smart suggestions
- Dashboard statistics
"""

import os
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List, Optional
from contextlib import asynccontextmanager

# Setup Django before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from django.db.models import Q, Count
from django.utils import timezone

from hotel.models import Room, RoomType, Guest, Booking, Payment


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================

class RoomTypeSchema(BaseModel):
    """نوع اتاق"""
    id: int
    name: str
    bed_type: str
    capacity: int
    base_price: Decimal
    
    class Config:
        from_attributes = True


class RoomSchema(BaseModel):
    """اتاق"""
    id: int
    room_number: str
    floor: int
    room_type: RoomTypeSchema
    status: str
    view: str
    is_active: bool
    nightly_rate: Decimal
    
    class Config:
        from_attributes = True


class RoomListSchema(BaseModel):
    """لیست اتاق‌ها"""
    id: int
    room_number: str
    floor: int
    room_type_name: str
    status: str
    view: str
    nightly_rate: Decimal


class GuestSchema(BaseModel):
    """مهمان"""
    id: int
    first_name: str
    last_name: str
    national_id: Optional[str] = None
    phone: str
    email: Optional[str] = None
    nationality: str


class GuestCreateSchema(BaseModel):
    """ایجاد مهمان جدید"""
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    national_id: Optional[str] = None
    passport_number: Optional[str] = None
    gender: str = "male"
    phone: str = Field(..., min_length=10, max_length=15)
    email: Optional[str] = None
    address: Optional[str] = None
    nationality: str = "ایرانی"


class BookingSchema(BaseModel):
    """رزرو"""
    id: int
    booking_number: str
    room_id: int
    room_number: str
    guest_id: int
    guest_name: str
    check_in_date: date
    check_out_date: date
    status: str
    adults: int
    children: int
    nights: int
    nightly_rate: Decimal
    total_amount: Decimal


class BookingCreateSchema(BaseModel):
    """ایجاد رزرو جدید"""
    room_id: int
    guest_id: int
    check_in_date: date
    check_out_date: date
    adults: int = Field(default=1, ge=1, le=10)
    children: int = Field(default=0, ge=0, le=10)
    service_charge: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")
    notes: Optional[str] = None
    
    @field_validator('check_out_date')
    @classmethod
    def checkout_after_checkin(cls, v, info):
        if 'check_in_date' in info.data and v <= info.data['check_in_date']:
            raise ValueError('تاریخ خروج باید بعد از تاریخ ورود باشد')
        return v


class AvailabilityCheckSchema(BaseModel):
    """بررسی موجودی"""
    check_in_date: date
    check_out_date: date
    guests: int = Field(default=2, ge=1, le=10)


class BestRoomSuggestion(BaseModel):
    """پیشنهاد بهترین اتاق"""
    room_id: int
    room_number: str
    room_type: str
    floor: int
    view: str
    capacity: int
    nightly_rate: Decimal
    total_price: Decimal
    score: float
    reason: str


class DashboardStats(BaseModel):
    """آمار داشبورد"""
    rooms_total: int
    rooms_clean: int
    rooms_dirty: int
    rooms_occupied: int
    rooms_maintenance: int
    today_checkins: int
    today_checkouts: int
    bookings_pending: int
    bookings_active: int
    guests_total: int


class CheckInOutRequest(BaseModel):
    """درخواست ورود/خروج"""
    booking_id: int


class RoomStatusUpdate(BaseModel):
    """بروزرسانی وضعیت اتاق"""
    status: str = Field(..., pattern="^(clean|dirty|occupied|maintenance)$")


# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    yield


app = FastAPI(
    title="سیستم مدیریت هتل - API",
    description="API برای مدیریت رزرواسیون و اتاق‌های هتل",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def check_room_availability(room_id: int, check_in: date, check_out: date, exclude_booking_id: int = None) -> bool:
    """
    Check if a room is available for the given date range.
    بررسی موجودی اتاق برای بازه زمانی مشخص
    
    A room is unavailable if there's any booking that overlaps:
    - Existing booking starts before our checkout AND ends after our checkin
    """
    query = Booking.objects.filter(
        room_id=room_id,
        status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED, Booking.Status.CHECKED_IN],
        check_in_date__lt=check_out,  # Starts before we leave
        check_out_date__gt=check_in,  # Ends after we arrive
    )
    
    if exclude_booking_id:
        query = query.exclude(pk=exclude_booking_id)
    
    return not query.exists()


def get_available_rooms(check_in: date, check_out: date, min_capacity: int = 1) -> List[Room]:
    """
    Get all available rooms for the given date range.
    دریافت اتاق‌های موجود برای بازه زمانی
    """
    # Get rooms with conflicting bookings
    conflicting_rooms = Booking.objects.filter(
        status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED, Booking.Status.CHECKED_IN],
        check_in_date__lt=check_out,
        check_out_date__gt=check_in,
    ).values_list('room_id', flat=True)
    
    # Get available rooms
    return Room.objects.filter(
        is_active=True,
        status__in=[Room.Status.CLEAN, Room.Status.DIRTY],
        room_type__capacity__gte=min_capacity,
    ).exclude(pk__in=conflicting_rooms).select_related('room_type')


def calculate_room_score(room: Room, guests: int, nights: int) -> tuple[float, str]:
    """
    Calculate a score for room suggestion.
    محاسبه امتیاز اتاق برای پیشنهاد
    
    Scoring factors:
    - Capacity match (penalty for over-capacity rooms)
    - View preference (sea > pool > garden > mountain > city > none)
    - Floor preference (higher floors slightly preferred)
    - Price efficiency
    """
    score = 100.0
    reasons = []
    
    # Capacity match (prefer rooms closest to guest count)
    capacity_diff = room.room_type.capacity - guests
    if capacity_diff == 0:
        score += 20
        reasons.append("ظرفیت دقیق")
    elif capacity_diff == 1:
        score += 10
        reasons.append("ظرفیت مناسب")
    elif capacity_diff > 2:
        score -= capacity_diff * 5
        reasons.append("ظرفیت بیشتر از نیاز")
    
    # View preference
    view_scores = {
        Room.View.SEA: 25,
        Room.View.POOL: 20,
        Room.View.GARDEN: 15,
        Room.View.MOUNTAIN: 12,
        Room.View.CITY: 8,
        Room.View.NONE: 0,
    }
    view_score = view_scores.get(room.view, 0)
    score += view_score
    if view_score >= 20:
        reasons.append(f"منظره {room.get_view_display()}")
    
    # Floor preference (higher floors slightly better)
    score += min(room.floor * 2, 10)
    
    # Room status (clean rooms preferred)
    if room.status == Room.Status.CLEAN:
        score += 15
        reasons.append("آماده")
    else:
        reasons.append("نیاز به آماده‌سازی")
    
    reason = " | ".join(reasons) if reasons else "پیشنهاد عمومی"
    return score, reason


# =============================================================================
# API ENDPOINTS - DASHBOARD
# =============================================================================

@app.get("/api/dashboard/stats", response_model=DashboardStats, tags=["Dashboard"])
async def get_dashboard_stats():
    """
    دریافت آمار داشبورد
    Get dashboard statistics
    """
    today = timezone.now().date()
    
    return DashboardStats(
        rooms_total=Room.objects.filter(is_active=True).count(),
        rooms_clean=Room.objects.filter(status=Room.Status.CLEAN, is_active=True).count(),
        rooms_dirty=Room.objects.filter(status=Room.Status.DIRTY, is_active=True).count(),
        rooms_occupied=Room.objects.filter(status=Room.Status.OCCUPIED, is_active=True).count(),
        rooms_maintenance=Room.objects.filter(status=Room.Status.MAINTENANCE, is_active=True).count(),
        today_checkins=Booking.objects.filter(
            check_in_date=today,
            status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED]
        ).count(),
        today_checkouts=Booking.objects.filter(
            check_out_date=today,
            status=Booking.Status.CHECKED_IN
        ).count(),
        bookings_pending=Booking.objects.filter(status=Booking.Status.PENDING).count(),
        bookings_active=Booking.objects.filter(status=Booking.Status.CHECKED_IN).count(),
        guests_total=Guest.objects.count(),
    )


# =============================================================================
# API ENDPOINTS - ROOMS
# =============================================================================

@app.get("/api/rooms", response_model=List[RoomListSchema], tags=["Rooms"])
async def list_rooms(
    status: Optional[str] = None,
    floor: Optional[int] = None,
    is_active: bool = True,
):
    """
    دریافت لیست اتاق‌ها
    Get list of rooms with optional filters
    """
    queryset = Room.objects.filter(is_active=is_active).select_related('room_type')
    
    if status:
        queryset = queryset.filter(status=status)
    if floor:
        queryset = queryset.filter(floor=floor)
    
    return [
        RoomListSchema(
            id=room.pk,
            room_number=room.room_number,
            floor=room.floor,
            room_type_name=room.room_type.name,
            status=room.status,
            view=room.view,
            nightly_rate=room.nightly_rate,
        )
        for room in queryset
    ]


@app.get("/api/rooms/{room_id}", response_model=RoomSchema, tags=["Rooms"])
async def get_room(room_id: int):
    """
    دریافت اطلاعات اتاق
    Get room details
    """
    try:
        room = Room.objects.select_related('room_type').get(pk=room_id)
        return RoomSchema(
            id=room.pk,
            room_number=room.room_number,
            floor=room.floor,
            room_type=RoomTypeSchema(
                id=room.room_type.pk,
                name=room.room_type.name,
                bed_type=room.room_type.bed_type,
                capacity=room.room_type.capacity,
                base_price=room.room_type.base_price,
            ),
            status=room.status,
            view=room.view,
            is_active=room.is_active,
            nightly_rate=room.nightly_rate,
        )
    except Room.DoesNotExist:
        raise HTTPException(status_code=404, detail="اتاق یافت نشد")


@app.patch("/api/rooms/{room_id}/status", tags=["Rooms"])
async def update_room_status(room_id: int, data: RoomStatusUpdate):
    """
    بروزرسانی وضعیت اتاق
    Update room status (clean/dirty/occupied/maintenance)
    """
    try:
        room = Room.objects.get(pk=room_id)
        room.status = data.status
        room.save()
        return {"message": "وضعیت اتاق بروزرسانی شد", "status": data.status}
    except Room.DoesNotExist:
        raise HTTPException(status_code=404, detail="اتاق یافت نشد")


@app.get("/api/rooms/available", response_model=List[RoomListSchema], tags=["Rooms"])
async def get_available_rooms_endpoint(
    check_in: date = Query(..., description="تاریخ ورود"),
    check_out: date = Query(..., description="تاریخ خروج"),
    guests: int = Query(default=2, ge=1, le=10, description="تعداد مهمانان"),
):
    """
    دریافت اتاق‌های موجود
    Get available rooms for date range
    """
    if check_out <= check_in:
        raise HTTPException(status_code=400, detail="تاریخ خروج باید بعد از تاریخ ورود باشد")
    
    rooms = get_available_rooms(check_in, check_out, guests)
    
    return [
        RoomListSchema(
            id=room.pk,
            room_number=room.room_number,
            floor=room.floor,
            room_type_name=room.room_type.name,
            status=room.status,
            view=room.view,
            nightly_rate=room.nightly_rate,
        )
        for room in rooms
    ]


# =============================================================================
# API ENDPOINTS - BEST ROOM ALGORITHM
# =============================================================================

@app.get("/api/rooms/suggest", response_model=List[BestRoomSuggestion], tags=["Smart Features"])
async def suggest_best_rooms(
    check_in: date = Query(..., description="تاریخ ورود"),
    check_out: date = Query(..., description="تاریخ خروج"),
    guests: int = Query(default=2, ge=1, le=10, description="تعداد مهمانان"),
    limit: int = Query(default=5, ge=1, le=10, description="تعداد پیشنهاد"),
):
    """
    پیشنهاد بهترین اتاق
    Suggest best rooms based on guest count and availability
    
    Algorithm considers:
    - Capacity match
    - Room view quality
    - Floor preference
    - Room cleanliness status
    """
    if check_out <= check_in:
        raise HTTPException(status_code=400, detail="تاریخ خروج باید بعد از تاریخ ورود باشد")
    
    nights = (check_out - check_in).days
    rooms = get_available_rooms(check_in, check_out, guests)
    
    # Calculate scores for each room
    suggestions = []
    for room in rooms:
        score, reason = calculate_room_score(room, guests, nights)
        total_price = room.nightly_rate * nights
        
        suggestions.append(BestRoomSuggestion(
            room_id=room.pk,
            room_number=room.room_number,
            room_type=room.room_type.name,
            floor=room.floor,
            view=room.view,
            capacity=room.room_type.capacity,
            nightly_rate=room.nightly_rate,
            total_price=total_price,
            score=score,
            reason=reason,
        ))
    
    # Sort by score (highest first) and return top N
    suggestions.sort(key=lambda x: x.score, reverse=True)
    return suggestions[:limit]


# =============================================================================
# API ENDPOINTS - GUESTS
# =============================================================================

@app.get("/api/guests", response_model=List[GuestSchema], tags=["Guests"])
async def list_guests(
    search: Optional[str] = None,
    limit: int = Query(default=50, le=100),
):
    """
    دریافت لیست مهمانان
    Get list of guests
    """
    queryset = Guest.objects.all()
    
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(national_id__icontains=search) |
            Q(phone__icontains=search)
        )
    
    return [
        GuestSchema(
            id=guest.pk,
            first_name=guest.first_name,
            last_name=guest.last_name,
            national_id=guest.national_id,
            phone=guest.phone,
            email=guest.email or None,
            nationality=guest.nationality,
        )
        for guest in queryset[:limit]
    ]


@app.post("/api/guests", response_model=GuestSchema, status_code=status.HTTP_201_CREATED, tags=["Guests"])
async def create_guest(data: GuestCreateSchema):
    """
    ثبت مهمان جدید
    Create new guest
    """
    # Check for duplicate national ID
    if data.national_id and Guest.objects.filter(national_id=data.national_id).exists():
        raise HTTPException(status_code=400, detail="مهمان با این کد ملی قبلاً ثبت شده است")
    
    guest = Guest.objects.create(**data.model_dump())
    
    return GuestSchema(
        id=guest.pk,
        first_name=guest.first_name,
        last_name=guest.last_name,
        national_id=guest.national_id,
        phone=guest.phone,
        email=guest.email or None,
        nationality=guest.nationality,
    )


# =============================================================================
# API ENDPOINTS - BOOKINGS
# =============================================================================

@app.get("/api/bookings", response_model=List[BookingSchema], tags=["Bookings"])
async def list_bookings(
    status: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    room_id: Optional[int] = None,
    limit: int = Query(default=50, le=100),
):
    """
    دریافت لیست رزروها
    Get list of bookings with filters
    """
    queryset = Booking.objects.select_related('room', 'guest').all()
    
    if status:
        queryset = queryset.filter(status=status)
    if from_date:
        queryset = queryset.filter(check_in_date__gte=from_date)
    if to_date:
        queryset = queryset.filter(check_out_date__lte=to_date)
    if room_id:
        queryset = queryset.filter(room_id=room_id)
    
    return [
        BookingSchema(
            id=booking.pk,
            booking_number=booking.booking_number,
            room_id=booking.room_id,
            room_number=booking.room.room_number,
            guest_id=booking.guest_id,
            guest_name=booking.guest.full_name,
            check_in_date=booking.check_in_date,
            check_out_date=booking.check_out_date,
            status=booking.status,
            adults=booking.adults,
            children=booking.children,
            nights=booking.nights,
            nightly_rate=booking.nightly_rate,
            total_amount=booking.total_amount,
        )
        for booking in queryset.order_by('-check_in_date')[:limit]
    ]


@app.post("/api/bookings", response_model=BookingSchema, status_code=status.HTTP_201_CREATED, tags=["Bookings"])
async def create_booking(data: BookingCreateSchema):
    """
    ایجاد رزرو جدید
    Create new booking with date overlap validation
    """
    # Validate room exists
    try:
        room = Room.objects.select_related('room_type').get(pk=data.room_id)
    except Room.DoesNotExist:
        raise HTTPException(status_code=404, detail="اتاق یافت نشد")
    
    # Validate guest exists
    try:
        guest = Guest.objects.get(pk=data.guest_id)
    except Guest.DoesNotExist:
        raise HTTPException(status_code=404, detail="مهمان یافت نشد")
    
    # Check room availability (date overlap validation)
    if not check_room_availability(data.room_id, data.check_in_date, data.check_out_date):
        raise HTTPException(
            status_code=400, 
            detail="اتاق در این بازه زمانی رزرو شده است"
        )
    
    # Check capacity
    total_guests = data.adults + data.children
    if total_guests > room.room_type.capacity:
        raise HTTPException(
            status_code=400,
            detail=f"ظرفیت اتاق ({room.room_type.capacity} نفر) کمتر از تعداد مهمانان است"
        )
    
    # Create booking
    booking = Booking.objects.create(
        room=room,
        guest=guest,
        check_in_date=data.check_in_date,
        check_out_date=data.check_out_date,
        adults=data.adults,
        children=data.children,
        nightly_rate=room.nightly_rate,
        service_charge=data.service_charge,
        discount=data.discount,
        notes=data.notes or "",
        status=Booking.Status.PENDING,
    )
    
    return BookingSchema(
        id=booking.pk,
        booking_number=booking.booking_number,
        room_id=booking.room_id,
        room_number=room.room_number,
        guest_id=booking.guest_id,
        guest_name=guest.full_name,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        status=booking.status,
        adults=booking.adults,
        children=booking.children,
        nights=booking.nights,
        nightly_rate=booking.nightly_rate,
        total_amount=booking.total_amount,
    )


@app.post("/api/bookings/{booking_id}/check-in", tags=["Bookings"])
async def check_in(booking_id: int):
    """
    ثبت ورود مهمان
    Process guest check-in
    """
    try:
        booking = Booking.objects.select_related('room').get(pk=booking_id)
    except Booking.DoesNotExist:
        raise HTTPException(status_code=404, detail="رزرو یافت نشد")
    
    if booking.status not in [Booking.Status.PENDING, Booking.Status.CONFIRMED]:
        raise HTTPException(status_code=400, detail="این رزرو قابل ورود نیست")
    
    # Update booking
    booking.status = Booking.Status.CHECKED_IN
    booking.actual_check_in = timezone.now()
    booking.save()
    
    # Update room status to occupied
    booking.room.status = Room.Status.OCCUPIED
    booking.room.save()
    
    return {
        "message": "ورود مهمان ثبت شد",
        "booking_number": booking.booking_number,
        "check_in_time": booking.actual_check_in.isoformat(),
    }


@app.post("/api/bookings/{booking_id}/check-out", tags=["Bookings"])
async def check_out(booking_id: int):
    """
    ثبت خروج مهمان
    Process guest check-out (auto-triggers room dirty status)
    """
    try:
        booking = Booking.objects.select_related('room').get(pk=booking_id)
    except Booking.DoesNotExist:
        raise HTTPException(status_code=404, detail="رزرو یافت نشد")
    
    if booking.status != Booking.Status.CHECKED_IN:
        raise HTTPException(status_code=400, detail="مهمان ورود نکرده است")
    
    # Update booking
    booking.status = Booking.Status.CHECKED_OUT
    booking.actual_check_out = timezone.now()
    booking.save()
    
    # Auto-trigger: Set room to dirty after checkout
    booking.room.status = Room.Status.DIRTY
    booking.room.save()
    
    return {
        "message": "خروج مهمان ثبت شد",
        "booking_number": booking.booking_number,
        "check_out_time": booking.actual_check_out.isoformat(),
        "total_amount": str(booking.total_amount),
    }


@app.post("/api/bookings/{booking_id}/cancel", tags=["Bookings"])
async def cancel_booking(booking_id: int):
    """
    لغو رزرو
    Cancel booking
    """
    try:
        booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        raise HTTPException(status_code=404, detail="رزرو یافت نشد")
    
    if booking.status == Booking.Status.CHECKED_IN:
        raise HTTPException(status_code=400, detail="امکان لغو رزرو پس از ورود وجود ندارد")
    
    if booking.status in [Booking.Status.CHECKED_OUT, Booking.Status.CANCELLED]:
        raise HTTPException(status_code=400, detail="این رزرو قبلاً تکمیل یا لغو شده است")
    
    booking.status = Booking.Status.CANCELLED
    booking.save()
    
    return {"message": "رزرو لغو شد", "booking_number": booking.booking_number}


# =============================================================================
# API ENDPOINTS - TAPE CHART DATA
# =============================================================================

@app.get("/api/tape-chart", tags=["Dashboard"])
async def get_tape_chart_data(
    start_date: date = Query(..., description="تاریخ شروع"),
    end_date: date = Query(..., description="تاریخ پایان"),
):
    """
    دریافت داده‌های نمودار نواری (Tape Chart)
    Get data for tape chart visualization
    
    Returns rooms and their bookings for the date range.
    """
    if end_date <= start_date:
        raise HTTPException(status_code=400, detail="تاریخ پایان باید بعد از تاریخ شروع باشد")
    
    rooms = Room.objects.filter(is_active=True).select_related('room_type').order_by('floor', 'room_number')
    
    bookings = Booking.objects.filter(
        status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED, Booking.Status.CHECKED_IN],
        check_in_date__lt=end_date,
        check_out_date__gt=start_date,
    ).select_related('guest', 'room')
    
    # Build booking map by room
    booking_map = {}
    for booking in bookings:
        if booking.room_id not in booking_map:
            booking_map[booking.room_id] = []
        booking_map[booking.room_id].append({
            "id": booking.pk,
            "booking_number": booking.booking_number,
            "guest_name": booking.guest.full_name,
            "check_in": booking.check_in_date.isoformat(),
            "check_out": booking.check_out_date.isoformat(),
            "status": booking.status,
            "nights": booking.nights,
        })
    
    # Build response
    result = []
    for room in rooms:
        result.append({
            "room_id": room.pk,
            "room_number": room.room_number,
            "floor": room.floor,
            "room_type": room.room_type.name,
            "status": room.status,
            "bookings": booking_map.get(room.pk, []),
        })
    
    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "rooms": result,
    }


# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.get("/api/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": timezone.now().isoformat()}
