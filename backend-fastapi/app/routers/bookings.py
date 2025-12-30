from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List
from datetime import date
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)

@router.post("/", response_model=schemas.BookingOut)
def create_booking(
    booking: schemas.BookingCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 1. Validate dates
    if booking.check_in >= booking.check_out:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date"
        )
    
    # 2. Check room existence and get rate
    room = db.query(models.Room).filter(models.Room.id == booking.room_id).first()
    if not room:
         raise HTTPException(status_code=404, detail="Room not found")
    
    # 3. Check for overlaps
    # Overlap if: (StartA <= EndB) and (EndA >= StartB)
    # Django model check was: check_in__lt=self.check_out, check_out__gt=self.check_in
    overlapping = db.query(models.Booking).filter(
        models.Booking.room_id == booking.room_id,
        models.Booking.check_in < booking.check_out,
        models.Booking.check_out > booking.check_in,
        models.Booking.status.notin_(['cancelled', 'no_show'])
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is already booked for these dates"
        )

    # 4. Calculate Price
    # Simple logic: days * base_rate (ignoring seasonal override for MVP speed, can be added)
    days = (booking.check_out - booking.check_in).days
    # Need to join RoomType to get rate
    # SQLAlchemy lazy load might need explicit join if not loaded
    # Room model in models.py defines relationship? Yes: room_type relationship
    if not room.room_type:
        # Load it if missing (depends on model definition)
        # Assuming eager load or lazy load works. room.room_type should work if definition is correct.
        pass
    
    # We didn't define relationship backref in RoomType, but Room has room_type_id and relationship
    # Let's query RoomType directly to be safe and faster
    room_type = db.query(models.RoomType).filter(models.RoomType.id == room.room_type_id).first()
    total_price = room_type.base_rate * days

    new_booking = models.Booking(
        guest_id=current_user.id,
        room_id=booking.room_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        status='reserved',
        total_price=total_price
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return new_booking

@router.get("/me", response_model=List[schemas.BookingOut])
def my_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Booking).filter(models.Booking.guest_id == current_user.id).all()
