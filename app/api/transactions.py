from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_general_session
from app.models.transactions import Transaction
from app.schemas.transactions import TransactionCreate, TransactionResponse
from app.services.transactions import create_transaction

app = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)

@app.post("/", response_model=TransactionResponse)
async def create(
    transaction: TransactionCreate,
    session: AsyncSession = Depends(get_general_session)
):
    return await create_transaction(transaction, session)