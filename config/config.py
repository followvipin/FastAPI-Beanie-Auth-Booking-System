# let's import some specific attribute, function  & class from required package and module
from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from models.user import User
from urllib.parse import quote_plus
from pymongo.server_api import ServerApi


# let's create a "Setting" class to connect with mongodb database
class Settings(BaseSettings):

    # database configurations
    # this class requires the database credentials to connect with mongodb atlas also if you want to connect it localhost machine you can use your local database credentials.

    # username: str= quote_plus("mongo_username")
    # password: str= quote_plus("mongo_password")
    # DATABASE_URL: Optional[str] = (
    #     "mongodb+srv://"
    #     + username
    #     + ":"
    #     + password
    #     + "@"
    #     + "mongo_username.hprvpha.mongodb.net/?retryWrites=true&w=majority"
    # )

    DATABASE_URL: Optional[str] = ("mongodb://localhost:27017")

    # for localhost use connection string "mongodb://localhost:27017"

    class Config:
        env_file = ".env.dev"
        from_attributes = True


# Initializes the MongoDB connection and sets up Beanie ORM with the User model
async def initiate_database():
    try:
        client = AsyncIOMotorClient(Settings().DATABASE_URL, server_api=ServerApi("1"))
        database = client["mongo_db"]
        await init_beanie(database, document_models=[User])
        print("Pinged your database deployment. You successfully connected to MongoDB!")

    except Exception as e:
        # Raise exception if something went wrong while connecting to the database server.
        print(e)
