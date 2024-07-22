from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from typing import Union, Optional
from beanie import PydanticObjectId
from datetime import datetime
from typing import Union
from bson.objectid import ObjectId as BsonObjectId

class User(Document):

    username: Union[str, None]
    email: Union[EmailStr, None]
    created_at: datetime

    # Let's add some addition attributes

    dob: Union[datetime, None]
    gender: Union[str, None]

    class Settings:
        name = "user"

