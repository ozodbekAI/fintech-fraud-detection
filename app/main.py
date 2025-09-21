from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from worker.producer import broker
from app.api.users import app as users_router
from app.api.transactions import app as transactions_router


app = FastAPI()


app.include_router(users_router)
app.include_router(transactions_router)

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

@app.on_event("startup")
async def startup_event():
    await broker.connect()
    print("Broker connected")

@app.on_event("shutdown")
async def shutdown_event():
    await broker.close()
    print("Broker disconnected")
