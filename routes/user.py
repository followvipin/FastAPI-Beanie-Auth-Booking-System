# let's import some specific attribute, function  & class from required package and module
from typing import Dict
# from auth.firebase import get_current_user
from routes.user import *
from database.user import *
from database.booking import (
    retrieve_bookings,
    retrieve_booking_history,
    retrieve_upcoming_bookings,
)
from beanie import PydanticObjectId
from fastapi import Body, APIRouter, Response, HTTPException
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import sign_jwt, decode_jwt
from fastapi.responses import JSONResponse
from fastapi import Depends
from models.user import *
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from config.config import Settings
from pymongo.server_api import ServerApi

router = APIRouter()
token_listener = JWTBearer()


@router.post("/signup/")
async def user_signup(response: Response, user: User = Body(...)):
    """
    Handles user signup by creating a new user if they do not already exist.

    Args:
        Body: The incoming request object containing user data payload.
        response (Response): The response object used to send back the result.

    Returns:
        JSONResponse: A JSON response indicating the result of the signup attempt.
    """
    # Extract the username from the user data
    username = user.username

    # Check if a user with the same username already exists in the collection
    user_exists = await user_collection.find_one(user_collection.username == username)

    if user_exists is None:

        try:
            # Attempt to add the new user to the database
            await add_new_user(user)

            # Prepare the response data for a successful signup
            response_data = {
                "status_code": "200",
                "message": "User created successfully!",
            }

            # Create and return a JSON response with the success message
            response = JSONResponse(content=response_data)
            return response
        except Exception as e:
            # Print the exception if there was an error during database operation
            print(e)
            # You might want to return an appropriate error response here

    else:
        # Prepare the response data indicating that the user already exists
        response_data = {"status_code": "409", "message": "User already exists!"}

        # Create and return a JSON response with the conflict message
        response = JSONResponse(content=response_data)
        return response


# Endpoint for user login, authenticating credentials and returning a JWT if successful.
@router.post("/login")
async def user_login(user_credentials: UserSignIn = Body(...)):
    """
    Handles user login by providing username and password.

    Returns:
        Token for authentication.
    """
    user_exists = await User.find_one(User.username == user_credentials.username)
    if user_exists:
        password = user_credentials.password
        if password:
            return sign_jwt(user_credentials.username)

        raise HTTPException(status_code=403, detail="Incorrect email or password")

    raise HTTPException(status_code=403, detail="Incorrect email or password")



# Endpoint to retrieve all users, accessible only to authenticated users via JWT token verification.
@router.get("/retrieve_all_users/", dependencies=[Depends(token_listener)])
async def get_all_users(credentials: HTTPBasicCredentials = Depends(token_listener)):
    """
    JWT Authentication required to access this endpoint.
    
    Returns:
        All the existing users in the database.
    """
    payload = decode_jwt(credentials)
    username = payload["user_id"]
    try:
        user_exists = await user_collection.find_one(
            user_collection.username == username
        )
        if user_exists:
            print("Welcome back!", username)
            try:
                all_users = await retrieve_all_users()
                return {
                    "status_code": 200,
                    "message": "all users are retrieved successfully!",
                    "all_user": all_users,
                }
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


# Endpoint to retrieve all users, accessible only to authenticated users via JWT token verification.
@router.get("/retrieve/active/bookings/", dependencies=[Depends(token_listener)])
async def get_my_bookings(credentials: HTTPBasicCredentials = Depends(token_listener)):
    """
    JWT Authentication required to access this endpoint.
    
    Returns:
        All the existing bookings of the user.
    """
    payload = decode_jwt(credentials)
    username = payload["user_id"]
    try:
        user_exists = await user_collection.find_one(
            user_collection.username == username
        )
        my_bookings = user_exists.bookings
        if user_exists:
            print("Welcome back!", username)
            try:
                my_bookings = await retrieve_bookings(my_bookings)
                return {
                    "status_code": 200,
                    "message": "all users are retrieved successfully!",
                    "all_user": my_bookings,
                }
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


# Endpoint to retrieve user's booking past history with calender view projection model.
@router.get("/calendar/history/bookings/", dependencies=[Depends(token_listener)])
async def get_booking_history(
    credentials: HTTPBasicCredentials = Depends(token_listener),
):
    """
    JWT Authentication required to access this endpoint.
    
    Returns:
        All the past bookings bookings of the user.
    """
    payload = decode_jwt(credentials)
    username = payload["user_id"]
    try:
        user_exists = await user_collection.find_one(
            user_collection.username == username
        )
        my_bookings = user_exists.bookings
        if user_exists:
            print("Welcome back!", username)
            try:
                my_bookings = await retrieve_booking_history(my_bookings)
                return {
                    "status_code": 200,
                    "message": "all users are retrieved successfully!",
                    "all_user": my_bookings,
                }
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


# Endpoint to retrieve user's upcoming bookings with calender view projection model.
@router.get("/calendar/upcoming/bookings/", dependencies=[Depends(token_listener)])
async def get_upcoming_bookings(
    credentials: HTTPBasicCredentials = Depends(token_listener),
):
    """
    JWT Authentication required to access this endpoint.
    
    Returns:
        All the active (not canceled) upcoming bookings of the user.
    """
    payload = decode_jwt(credentials)
    username = payload["user_id"]
    try:
        user_exists = await user_collection.find_one(
            user_collection.username == username
        )
        my_bookings = user_exists.bookings
        if user_exists:
            print("Welcome back!", username)
            try:
                my_bookings = await retrieve_upcoming_bookings(my_bookings)
                return {
                    "status_code": 200,
                    "message": "Upcoming bookings retrieved successfully!",
                    "Upcoming_Booking": my_bookings,
                }
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


"""#Endpoint for adding a firebase id to the user document.
   #Endpoint can only be used for firebase google authentication purpose.

@router.get("/add/firebaseid/")
async def add_friebaseid(credentials: HTTPBasicCredentials = Depends(token_listener),current_user: Dict = Depends(get_current_user)):
    payload = decode_jwt(credentials)
    username = payload["user_id"]
    firebase_id = current_user.get("user_id")
    try:
        user_exists = await user_collection.find_one(
            user_collection.username == username
        )
        if user_exists:
            print("Welcome back!", username)
        uid=user_exists.id
        try:
            await update_user_data(uid, {"firebase":firebase_id})
        except Exception as e:
            print(e)

    except Exception as e:
            print(e)"""