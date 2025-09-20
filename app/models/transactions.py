from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey
from datetime import datetime
from app.core.database import Base
import enum
import uuid


class TransactionStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    suspicious = "suspicious"

created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[float]
    status: Mapped[TransactionStatus] = mapped_column(default=TransactionStatus.pending)
    created_at: Mapped[datetime] = created_at
    updated_at: Mapped[datetime] = updated_at