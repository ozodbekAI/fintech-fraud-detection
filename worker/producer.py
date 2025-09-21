from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transactions import Transaction, TransactionStatus
from app.schemas.transactions import TransactionCreate, TransactionResponse
import uuid
import datetime

broker = RabbitBroker(url="amqp://admin:admin@rabbitmq:5672/")


async def create_transaction(data, queue):

    await broker.publish(message=data, queue="transactions_queue")

