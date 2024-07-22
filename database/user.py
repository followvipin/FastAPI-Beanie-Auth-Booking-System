# let's import some specific attribute, function  & class from required package and module
from models.user import User
from typing import List

# Set the `user_collection` to the User model for database operations
user_collection = User


# Asynchronously creates a new user in the database from the provided user dictionary payload.
async def add_user(user_dict: dict):
    user = User(**user_dict)
    try:
        user = await user.create()
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