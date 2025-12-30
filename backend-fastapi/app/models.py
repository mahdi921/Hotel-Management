from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Numeric, Text, JSON
from sqlalchemy.orm import relationship
from .database import Base

# Mirroring Django's 'users_user' table
class User(Base):
    __tablename__ = "users_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String)
    # Mapping other required fields would go here if needed for API

# Mirroring 'django_session'
class DjangoSession(Base):
    __tablename__ = "django_session"
    session_key = Column(String, primary_key=True)
    session_data = Column(Text)
    expire_date = Column(DateTime)

# Mirroring 'rooms_room'
class RoomType(Base):
    __tablename__ = "rooms_roomtype"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    base_rate = Column(Numeric)
    
class Room(Base):
    __tablename__ = "rooms_room"
    id = Column(Integer, primary_key=True)
    room_number = Column(String, unique=True)
    room_type_id = Column(Integer, ForeignKey("rooms_roomtype.id"))
    status = Column(String)
    
    room_type = relationship("RoomType")

# Mirroring 'bookings_booking'
class Booking(Base):
    __tablename__ = "bookings_booking"
    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey("users_user.id"))
    room_id = Column(Integer, ForeignKey("rooms_room.id"))
    check_in = Column(Date)
    check_out = Column(Date)
    status = Column(String)
    total_price = Column(Numeric)

    room = relationship("Room")
    guest = relationship("User")
