from fastapi import FastAPI
from config.config import initiate_database
from routes.user import router as UserRouter
from routes.booking import router as BookingRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Define a context manager to handle startup tasks, such as initializing the database
@asynccontextmanager
async def start_app(app: FastAPI):
    await initiate_database()  # Initialize the database connection
    yield  # Proceed to the next operation

# Create an instance of the FastAPI application and set up the lifespan event
app = FastAPI(lifespan=start_app)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Disallow credentials such as cookies or HTTP authentication
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allowed HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "status_code": 200,
        "message": "Welcome to Booking System."  # Welcome message
    }

# Include the user routes with a prefix and tags for categorization
app.include_router(UserRouter, tags=["User"], prefix="/user")

# Include the booking routes with a prefix and tags for categorization
app.include_router(BookingRouter, tags=["Booking"], prefix="/booking")
