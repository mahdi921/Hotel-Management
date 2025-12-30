"""
Hotel Management System - Admin Configuration
Professional Admin Panel with django-unfold

This module configures the admin interface with:
- Custom dashboard widgets (Rooms to Clean, Today's Check-ins)
- Persian/Farsi labels throughout
- Modern, commercial-grade UI
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Count, Q
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import User, RoomType, Room, Guest, Booking, Payment


def dashboard_callback(request, context):
    """
    Dashboard callback for django-unfold.
    Provides data for dashboard widgets.
    داده‌های داشبورد مدیریت
    """
    today = timezone.now().date()
    
    # Statistics for dashboard
    context.update({
        # Room Statistics
        "rooms_total": Room.objects.filter(is_active=True).count(),
        "rooms_clean": Room.objects.filter(status=Room.Status.CLEAN, is_active=True).count(),
        "rooms_dirty": Room.objects.filter(status=Room.Status.DIRTY, is_active=True).count(),
        "rooms_occupied": Room.objects.filter(status=Room.Status.OCCUPIED, is_active=True).count(),
        "rooms_maintenance": Room.objects.filter(status=Room.Status.MAINTENANCE, is_active=True).count(),
        
        # Today's Operations
        "today_checkins": Booking.objects.filter(
            check_in_date=today,
            status__in=[Booking.Status.CONFIRMED, Booking.Status.PENDING]
        ).count(),
        "today_checkouts": Booking.objects.filter(
            check_out_date=today,
            status=Booking.Status.CHECKED_IN
        ).count(),
        
        # Booking Statistics
        "bookings_pending": Booking.objects.filter(status=Booking.Status.PENDING).count(),
        "bookings_active": Booking.objects.filter(status=Booking.Status.CHECKED_IN).count(),
        
        # Guest Statistics  
        "guests_total": Guest.objects.count(),
        
        # Recent bookings
        "recent_bookings": Booking.objects.select_related('guest', 'room').order_by('-created_at')[:5],
        
        # Rooms needing attention
        "rooms_to_clean": Room.objects.filter(status=Room.Status.DIRTY, is_active=True)[:5],
    })
    
    return context


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """
    Custom User Admin.
    مدیریت کاربران سیستم
    """
    list_display = ['username', 'get_full_name', 'role', 'phone', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    ordering = ['username']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('اطلاعات شخصی'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        (_('نقش و دسترسی'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('تاریخ‌ها'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'phone'),
        }),
    )
    
    @display(description=_('نام کامل'))
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


@admin.register(RoomType)
class RoomTypeAdmin(ModelAdmin):
    """
    Room Type Admin.
    مدیریت انواع اتاق
    """
    list_display = ['name', 'bed_type', 'capacity', 'display_price', 'room_count']
    list_filter = ['bed_type']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    @display(description=_('قیمت شبانه'))
    def display_price(self, obj):
        return f"{obj.base_price:,.0f} ریال"
    
    @display(description=_('تعداد اتاق'))
    def room_count(self, obj):
        return obj.rooms.filter(is_active=True).count()


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    """
    Room Admin.
    مدیریت اتاق‌ها
    """
    list_display = ['room_number', 'floor', 'room_type', 'display_status', 'view', 'is_active']
    list_filter = ['status', 'floor', 'room_type', 'view', 'is_active']
    search_fields = ['room_number', 'notes']
    ordering = ['floor', 'room_number']
    list_editable = ['status']
    
    fieldsets = (
        (_('اطلاعات اتاق'), {'fields': ('room_number', 'floor', 'room_type')}),
        (_('وضعیت'), {'fields': ('status', 'view', 'is_active')}),
        (_('یادداشت'), {'fields': ('notes',)}),
    )
    
    @display(description=_('وضعیت'), label={
        Room.Status.CLEAN: "success",
        Room.Status.DIRTY: "warning", 
        Room.Status.OCCUPIED: "info",
        Room.Status.MAINTENANCE: "danger",
    })
    def display_status(self, obj):
        return obj.status


@admin.register(Guest)
class GuestAdmin(ModelAdmin):
    """
    Guest Admin.
    مدیریت مهمانان
    """
    list_display = ['full_name', 'national_id', 'phone', 'nationality', 'booking_count', 'created_at']
    list_filter = ['nationality', 'gender', 'created_at']
    search_fields = ['first_name', 'last_name', 'national_id', 'passport_number', 'phone', 'email']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('اطلاعات شخصی'), {'fields': ('first_name', 'last_name', 'gender', 'date_of_birth', 'nationality')}),
        (_('مدارک شناسایی'), {'fields': ('national_id', 'passport_number')}),
        (_('اطلاعات تماس'), {'fields': ('phone', 'email', 'address')}),
        (_('یادداشت'), {'fields': ('notes',)}),
    )
    
    @display(description=_('نام کامل'))
    def full_name(self, obj):
        return obj.full_name
    
    @display(description=_('تعداد رزرو'))
    def booking_count(self, obj):
        return obj.bookings.count()


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    """
    Booking Admin.
    مدیریت رزروها
    """
    list_display = [
        'booking_number', 'guest', 'room', 'check_in_date', 'check_out_date',
        'nights', 'display_status', 'display_total'
    ]
    list_filter = ['status', 'check_in_date', 'room__room_type']
    search_fields = ['booking_number', 'guest__first_name', 'guest__last_name', 'room__room_number']
    ordering = ['-check_in_date']
    date_hierarchy = 'check_in_date'
    readonly_fields = ['booking_number', 'created_at', 'updated_at', 'nights', 'total_amount']
    autocomplete_fields = ['guest', 'room']
    
    fieldsets = (
        (_('اطلاعات رزرو'), {'fields': ('booking_number', 'guest', 'room', 'created_by')}),
        (_('تاریخ‌ها'), {'fields': ('check_in_date', 'check_out_date', 'actual_check_in', 'actual_check_out')}),
        (_('وضعیت'), {'fields': ('status', 'adults', 'children')}),
        (_('مالی'), {'fields': ('nightly_rate', 'service_charge', 'discount')}),
        (_('یادداشت'), {'fields': ('notes',)}),
        (_('متادیتا'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    @display(description=_('وضعیت'), label={
        Booking.Status.PENDING: "warning",
        Booking.Status.CONFIRMED: "info",
        Booking.Status.CHECKED_IN: "success",
        Booking.Status.CHECKED_OUT: "default",
        Booking.Status.CANCELLED: "danger",
        Booking.Status.NO_SHOW: "danger",
    })
    def display_status(self, obj):
        return obj.status
    
    @display(description=_('شب'))
    def nights(self, obj):
        return obj.nights
    
    @display(description=_('مبلغ کل'))
    def display_total(self, obj):
        return f"{obj.total_amount:,.0f} ریال"
    
    def save_model(self, request, obj, form, change):
        if not change:  # New booking
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    """
    Payment Admin.
    مدیریت پرداخت‌ها
    """
    list_display = ['booking', 'display_amount', 'method', 'display_status', 'received_by', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['booking__booking_number', 'reference_number']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    autocomplete_fields = ['booking']
    
    fieldsets = (
        (_('اطلاعات پرداخت'), {'fields': ('booking', 'amount', 'method')}),
        (_('وضعیت'), {'fields': ('status', 'reference_number', 'received_by')}),
        (_('یادداشت'), {'fields': ('notes',)}),
    )
    
    @display(description=_('مبلغ'))
    def display_amount(self, obj):
        return f"{obj.amount:,.0f} ریال"
    
    @display(description=_('وضعیت'), label={
        Payment.Status.PENDING: "warning",
        Payment.Status.COMPLETED: "success",
        Payment.Status.FAILED: "danger",
        Payment.Status.REFUNDED: "info",
    })
    def display_status(self, obj):
        return obj.status
    
    def save_model(self, request, obj, form, change):
        if not change:  # New payment
            obj.received_by = request.user
        super().save_model(request, obj, form, change)
