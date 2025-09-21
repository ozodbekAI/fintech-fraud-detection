from fastapi import HTTPException
from sqlalchemy import select
from app.core.security import SecurityManager
from sqlalchemy.ext.asyncio import AsyncSession
from faststream.rabbit import RabbitBroker
from app.models.transactions import Transaction, TransactionStatus
from app.schemas.transactions import TransactionCreate, TransactionResponse
from worker.producer import create_transaction as produce_transaction

class TransactionService:
    def __init__(self,
                 session: AsyncSession):
        self.session = session

    async def create_transaction(self, transaction: TransactionCreate) -> TransactionResponse:
        transaction_record = Transaction(
            sender_id=transaction.sender_id,
            receiver_id=transaction.receiver_id,
            amount=transaction.amount,
            status=TransactionStatus.pending,
        )
        self.session.add(transaction_record)
        await self.session.commit()
        await self.session.refresh(transaction_record)

        await produce_transaction(
            {
                "id": transaction_record.id,
                "sender_id": transaction_record.sender_id,
                "receiver_id": transaction_record.receiver_id,
                "amount": transaction_record.amount,
                "status": transaction_record.status,
            },
            queue="transactions_queue"
        )

        return TransactionResponse.from_orm(transaction_record)

    async def get_transaction_by_id(self, transaction_id: int):
        result = await self.session.execute(select(Transaction).filter(Transaction.id == transaction_id))
        transaction = result.scalars().first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return TransactionResponse.from_orm(transaction)


    async def get_transaction_by_id(self, transaction_id: int):
        result = await self.session.execute(select(Transaction).filter(Transaction.id == transaction_id))
        transaction = result.scalars().first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    
    async def get_all_transactions(self):
        result = await self.session.execute(select(Transaction))
        transactions = result.scalars().all()
        return transactions
    
    async def update_transaction_status(self, transaction_id: int, status: TransactionStatus):
        transaction = await self.get_transaction_by_id(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        transaction.status = status
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return TransactionResponse.from_orm(transaction)
    