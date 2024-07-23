# let's import some specific attribute, function  & class from required package and module
from datetime import timedelta
from routes.user import *
from database.user import *
from database.booking import *
from beanie import PydanticObjectId
from fastapi import Body, APIRouter, Response, HTTPException
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import sign_jwt, decode_jwt
from fastapi.responses import JSONResponse
from fastapi import Depends
from models.user import *
from models.booking import *
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from config.config import Settings
from pymongo.server_api import ServerApi

router = APIRouter()
token_listener = JWTBearer()

#this endpoint is used for creating a booking with booking time validation.
@router.post("/create_booking/", dependencies=[Depends(token_listener)])
async def add_new_booking(
    response: Response,
    booking: Booking = Body(...),
    credentials: HTTPBasicCredentials = Depends(token_listener),
):
    payload = decode_jwt(credentials)
    username = payload["user_id"]
    try:
        user_exists = await user_collection.find_one(
            user_collection.username == username
        )
        uid = user_exists.id
        user_bookings = user_exists.bookings
        current_booking_time = booking.booking_time
        try:
            booked = await validate_booking(current_booking_time)
            print("booked!")
            if booked == None:
                if booking.is_recurring==True:
                    
                    while current_booking_time <= booking.recurrence_end_date:
                        booking_dict: Booking = {
                            "user_id": uid,
                            "name": username,
                            "description": booking.description,
                            "booking_time": current_booking_time,
                            "created_at": datetime.now(),
                            "is_recurring": booking.is_recurring,
                            "recurrence_frequency": booking.recurrence_frequency,
                            "recurrence_end_date": booking.recurrence_end_date,
                            "canceled": booking.canceled
                            }
                        create_booking = await add_booking(booking_dict)
                        print(create_booking)
                        if create_booking:
                            user_bookings.append(create_booking.id)
                        await update_user_data(uid, {"bookings": user_bookings})
                        if booking.recurrence_frequency == "daily":
                            current_time += timedelta(days=1)
                        elif booking.recurrence_frequency == "weekly":
                            current_time += timedelta(weeks=1)
                        elif booking.recurrence_frequency == "monthly":
                            current_time += timedelta(weeks=4) 
                    response_data = {
                        "status_code": "200",
                        "message": "Booking created successfully!",
                    }

                    # Create and return a JSON response with the success message
                    response = JSONResponse(content=response_data)
                    return response
                else:
                    booking_dict: Booking = {
                            "user_id": uid,
                            "name": username,
                            "description": booking.description,
                            "booking_time": booking.booking_time,
                            "created_at": datetime.now(),
                            "is_recurring": booking.is_recurring,
                            "recurrence_frequency": booking.recurrence_frequency,
                            "recurrence_end_date": booking.recurrence_end_date,
                            "canceled": booking.canceled
                            }
                    create_booking = await add_booking(booking_dict)
                    print(create_booking)
                    if create_booking:
                        user_bookings.append(create_booking.id)
                    await update_user_data(uid, {"bookings": user_bookings})
                    response_data = {
                        "status_code": "200",
                        "message": "Booking created successfully!",
                    }

                    # Create and return a JSON response with the success message
                    response = JSONResponse(content=response_data)
                    return response
            else:
                response_data = {
                        "status_code": "400",
                        "message": "Booking slot unavailable!",
                    }

                    # Create and return a JSON response with the success message
                response = JSONResponse(content=response_data)
                return response

        except Exception as e:
            print(e)
        
    except Exception as e:
        print(e)
    
    
    


# Endpoint to retrieve all users, accessible only to authenticated users via JWT token verification.
@router.put("/modify_booking/{booking_id}/", dependencies=[Depends(token_listener)])
async def update_booking(
    booking_id: PydanticObjectId,
    credentials: HTTPBasicCredentials = Depends(token_listener),
    modifications: UpdateBooking = Body(...),
):
    payload = decode_jwt(credentials)
    username = payload["user_id"]
    try:
        user_exists = await user_collection.find_one(
            user_collection.username == username
        )
        if user_exists:
            booked = await validate_booking(modifications.booking_time)
            if booked == None:
                try:
                    updated_booking = await update_booking_data(
                        booking_id, {"booking_time": modifications.booking_time}
                    )
                    return {
                        "status_code": 200,
                        "message": "Booking updated successfully!",
                        "modified_booking": updated_booking,
                    }
                except Exception as e:
                    print(e)
            else:
                response_data = {
                        "status_code": "400",
                        "message": "Booking slot unavailable!",
                    }

                    # Create and return a JSON response with the success message
                response = JSONResponse(content=response_data)
                return response
    except Exception as e:
        print(e)

    

# Endpoint to retrieve all users, accessible only to authenticated users via JWT token verification.
@router.put("/cancle_booking/{booking_id}/", dependencies=[Depends(token_listener)])
async def cancle_booking(
    booking_id: PydanticObjectId,
    credentials: HTTPBasicCredentials = Depends(token_listener),
):
    payload = decode_jwt(credentials)
    username = payload["user_id"]
    try:
        user_exists = await user_collection.find_one(
            user_collection.username == username
        )
        if user_exists:
            try:
                updated_booking = await update_booking_data(
                    booking_id, {"canceled": True}
                )
                return {
                    "status_code": 200,
                    "message": "Booking canceled successfully!",
                    "modified_booking": updated_booking,
                }
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
