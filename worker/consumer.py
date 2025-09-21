from faststream import FastStream
from faststream.rabbit import RabbitBroker
from app.models.transactions import Transaction, TransactionStatus
from worker.fraud_checker import fraud_check
from app.core.database import session_maker
from worker.producer import broker

app = FastStream(broker=broker)

@broker.subscriber(queue="transactions_queue")
async def process_transaction(message: dict):
    print(f"Received message: {message}")
    async with session_maker() as session:
        transaction = await session.get(Transaction, message["id"])
        if not transaction:
            print(f"Transaction {message['id']} not found in DB")
            return

        # Fraud tekshirish
        is_fraud = fraud_check(transaction)

        if is_fraud:
            transaction.status = TransactionStatus.suspicious
        else:
            transaction.status = TransactionStatus.success

        await session.commit()