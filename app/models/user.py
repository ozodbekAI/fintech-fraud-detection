from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base):
    
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    full_name: Mapped[str] 
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    balance: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = created_at
    updated_at: Mapped[datetime] = updated_at

