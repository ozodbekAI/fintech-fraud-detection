from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transactions import Transaction, TransactionStatus
from app.schemas.transactions import TransactionCreate, TransactionResponse
import uuid
import datetime

broker = RabbitBroker()


async def create_transaction(transaction: TransactionCreate, session: AsyncSession) -> TransactionResponse:
    transaction_record = Transaction(
        sender_id=transaction.sender_id,
        receiver_id=transaction.receiver_id,
        amount=transaction.amount,
        status=TransactionStatus.pending,
    )
    session.add(transaction_record)
    await session.commit()
    await session.refresh(transaction_record)


    await broker.publish(
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