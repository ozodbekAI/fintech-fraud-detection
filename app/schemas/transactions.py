from datetime import datetime
from pydantic import BaseModel

from app.models.transactions import TransactionStatus


class TransactionCreate(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float


class TransactionResponse(BaseModel):
    id: str
    sender_id: int
    receiver_id: int
    amount: float
    status: TransactionStatus
    created_at: datetime

    class Config:
        from_attributes = True