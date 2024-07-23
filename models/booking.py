from typing import Optional
from beanie import Document, PydanticObjectId
from datetime import datetime
from pydantic import BaseModel

class Booking(Document):
    """
    Represents a booking document.
    """
    user_id: PydanticObjectId
    name: str
    description: str
    booking_time: datetime
    created_at: datetime
    is_recurring: bool = False
    recurrence_frequency: Optional[str] = None
    recurrence_end_date: Optional[datetime] = None
    canceled: bool = False

    class Settings:
        name = "booking"

class UpdateBooking(BaseModel):
    """
    Represents an update to a booking.
    """
    booking_time: datetime

class CalendarView(BaseModel):
    """
    Represents a calendar view.
    """
    description: str
    booking_time: datetime
    canceled: bool
