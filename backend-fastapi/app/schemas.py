from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import date

class RoomTypeBase(BaseModel):
    name: str
    base_rate: Decimal

class RoomTypeOut(RoomTypeBase):
    id: int
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    room_number: str
    status: str

class RoomOut(RoomBase):
    id: int
    room_type: RoomTypeOut
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    room_id: int
    check_in: date
    check_out: date

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    status: str
    total_price: Decimal
    guest_id: int

    class Config:
        from_attributes = True
