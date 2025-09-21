from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_general_session
from app.models.transactions import Transaction
from app.schemas.transactions import TransactionCreate, TransactionResponse
from app.services.transactions import TransactionService

app = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)

@app.post("/", response_model=TransactionResponse)
async def create(
    transaction: TransactionCreate,
    session: AsyncSession = Depends(get_general_session)
):
    service = TransactionService(session)
    return await service.create_transaction(transaction)

@app.get("/", response_model=list[TransactionResponse])
async def get_all_transactions(
    session: AsyncSession = Depends(get_general_session)
):
    service = TransactionService(session)
    return await service.get_all_transactions()


@app.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    session: AsyncSession = Depends(get_general_session)
):
    service = TransactionService(session)
    return await service.get_transaction_by_id(transaction_id)

