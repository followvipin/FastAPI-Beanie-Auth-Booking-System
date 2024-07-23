# let's import some specific attribute, function  & class from required package and module
from datetime import datetime
from typing import List, Union
from beanie import PydanticObjectId
from models.booking import *
from models.user import User

# from typing import List

# Set the `user_collection` to the User model for database operations
booking_collection = Booking


# Asynchronously creates a new booking in the database from the provided user dictionary payload.
async def add_booking(booking_dict: dict):
    booking = Booking(**booking_dict)
    try:
        booking = await booking.create()
        return booking
    except Exception as e:
        print(e)


# This function creates a new booking using the provided 'new_booking' object.
async def add_new_booking(new_booking: Booking) -> Booking:
    try:
        booking = await new_booking.create()
        return booking
    except Exception as e:
        print(e)


# This asynchronous function updates booking data based on the provided 'id' and 'data'.
async def update_booking_data(id: PydanticObjectId, data: dict) -> Union[bool, Booking]:
    body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in body.items()}}
    booking = await booking_collection.get(id)
    if booking:
        await booking.update(update_query)
        return booking
    return False


# This asynchronous function validates a booking based on the provided 'booking_time'.
async def validate_booking(booking_time: datetime) -> Union[Booking, None]:
    """
    It checks if a booking exists (not canceled) for the specified time and returns it,
    or returns None if no booking is found or an exception occurs.
    """
    try:
        booked = await booking_collection.find_one(
            {"booking_time": booking_time, "canceled": False}
        )
        if booked:
            return booked
        else:
            return None
    except Exception as e:
        print(e)

#this function return the complete list of a user bookings.
async def retrieve_bookings(bookings: list) -> List[Booking]:
    try:
        my_bookings = (
            await booking_collection.find({"_id": {"$in": bookings}})
            .sort("-created_at")
            .to_list()
        )

        return my_bookings
    except Exception as e:
        print(e)

#this function returns the list of past bookings.
async def retrieve_booking_history(bookings: list) -> List[Booking]:
    try:
        current_time = datetime.now()
        my_bookings = (
            await booking_collection.find(
                {"_id": {"$in": bookings}, "booking_time": {"$lte": current_time}},
                projection_model=CalendarView,
            )
            .sort("-booking_time")
            .to_list()
        )

        return my_bookings
    except Exception as e:
        print(e)

#this function returns the list of upcoming bookings.
async def retrieve_upcoming_bookings(bookings: list) -> List[Booking]:
    try:
        current_time = datetime.now()
        my_bookings = (
            await booking_collection.find(
                {
                    "_id": {"$in": bookings},
                    "canceled": False,
                    "booking_time": {"$gt": current_time},
                },
                projection_model=CalendarView,
            )
            .sort("booking_time")
            .to_list()
        )

        return my_bookings
    except Exception as e:
        print(e)
