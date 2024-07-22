from fastapi import FastAPI
from config.config import initiate_database
from routes.user import router as UserRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def start_app(app: FastAPI):
    await initiate_database()
    yield

app = FastAPI(lifespan=start_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {
        "status_code":200,
        "message":"Welcome to Booking System."
    }

app.include_router(UserRouter, tags=["User"], prefix="/user")
