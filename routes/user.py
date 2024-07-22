# let's import some specific attribute, function  & class from required package and module
from datetime import datetime
from routes.user import *
from database.user import *
from beanie import PydanticObjectId
from fastapi import (
    APIRouter,
    Request,
    Response
)
from fastapi.responses import JSONResponse
from fastapi import Depends
from models.user import User
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from config.config import Settings
from pymongo.server_api import ServerApi

router = APIRouter()

@router.post("/signup")
async def user_signup(request: Request, response: Response):
    """
    Handles user signup by creating a new user if they do not already exist.

    Args:
        request (Request): The incoming request object containing user data payload.
        response (Response): The response object used to send back the result.

    Returns:
        JSONResponse: A JSON response indicating the result of the signup attempt.
    """
    # Parse the incoming JSON request body into a Python dictionary
    user = await request.json()
    
    # Convert the user data to a format suitable for encoding
    data = jsonable_encoder(user)
    
    # Extract the username from the user data
    username = data["username"]
    
    # Check if a user with the same username already exists in the collection
    user_exists = await user_collection.find_one(
        user_collection.username == username
    )
    
    if user_exists is None:
        # Extract additional user information from the data
        email = data["email"]
        dob = data["dob"]
        gender = data["gender"]

        # Create a dictionary representing the new user to be added
        user_dict: User = {
            "username": username,
            "email": email,
            "dob": dob,
            "gender": gender,
            "created_at": datetime.now(),
        }

        try:
            # Attempt to add the new user to the database
            await add_user(user_dict)
            
            # Prepare the response data for a successful signup
            response_data = {
                "status_code": "200",
                "message": "User created successfully!"
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
        response_data = {
            "status_code": "409",
            "message": "User already exists!"
        }

        # Create and return a JSON response with the conflict message
        response = JSONResponse(content=response_data)
        return response

@router.get("/retrieve_all_users/")
async def get_all_users():
    try:
        all_users = await retrieve_all_users()
        return {
            "status_code":200,
            "message":"all users are retrieved successfully!",
            "all_user": all_users
        }
    except Exception as e:
        print(e)
