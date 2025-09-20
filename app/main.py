from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.users import app as users_router
from app.core.database import create_database

app = FastAPI()


app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Welcome to the Fintech Fraud Detection API"}


@app.post("/create-database/")
async def create_database():
    await create_database()
    return {"message": "Database created successfully"}