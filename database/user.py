# let's import some specific attribute, function  & class from required package and module
from beanie import PydanticObjectId
from models.user import User
from models.booking import Booking
from typing import List, Union

# Set the `user_collection` to the User model for database operations
user_collection = User
booking_collection = Booking


# Asynchronously creates a new user in the database from the provided user dictionary payload.
async def add_new_user(new_user: User) -> User:
    try:
        user = await new_user.create()
        return user
    except Exception as e:
        print(e)


# Retrieves all user documents from the MongoDB collection and returns them as a list of User objects.
async def retrieve_all_users() -> List[User]:
    try:
        users = await user_collection.all().to_list()
        return users
    except Exception as e:
        print(e)


#This function efficiently updates user data in a MongoDB collection
async def update_user_data(id: PydanticObjectId, data: dict) -> Union[bool, User]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    user = await user_collection.get(id)
    if user:
        await user.update(update_query)
        return user
    return False
