import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from worker.producer import broker
from app.api.users import app as users_router
from app.api.transactions import app as transactions_router

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fintech Fraud Detection API",
    description="API for fraud detection in fintech transactions",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics instrumentation
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Router'larni qo'shish
app.include_router(users_router)
app.include_router(transactions_router)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Fintech Fraud Detection API"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "fintech-fraud-detection"}

@app.on_event("startup")
async def startup_event():
    try:
        await broker.connect()
        logger.info("Broker connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect broker: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    try:
        await broker.close()
        logger.info("Broker disconnected successfully")
    except Exception as e:
        logger.error(f"Error disconnecting broker: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8080, 
        reload=False, 
        workers=1,
        log_level="info"
    )