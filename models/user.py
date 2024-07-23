from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from typing import Union
from beanie import PydanticObjectId
from datetime import datetime
from typing import Union

class User(Document):
    """
    Represents a user document.
    """
    username: Union[str, None]
    email: Union[EmailStr, None]
    password: Union[str, None]
    created_at: datetime

    # Additional attributes
    firebase_id: Union[str, None]
    dob: Union[datetime, None]
    gender: Union[str, None]
    bookings: Union[list[PydanticObjectId], None]

    class Settings:
        name = "user"

class UserSignIn(BaseModel):
    """
    Represents user sign-in credentials.
    """
    username: str
    password: str
