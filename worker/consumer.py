from faststream import FastStream
from faststream.rabbit import RabbitBroker
from app.models.transactions import Transaction, TransactionStatus
from worker.fraud_checker import fraud_check
from app.core.database import session_marker

broker = RabbitBroker()
app = FastStream(broker=broker)

@broker.subscribe(queue="transactions_queue")
async def process_transaction(message: dict):
    async with session_marker() as session:
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