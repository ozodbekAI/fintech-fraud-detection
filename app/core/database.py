from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings



postgres_url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


class Base(DeclarativeBase):
    pass


def get_async_engine():
    return create_async_engine(
        settings.database_url,
        future=True,
        echo=False,
    )


def get_general_session_maker() -> async_sessionmaker[AsyncSession]:
    engine = get_async_engine()
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,  # Prevent object expiration after commit
    )

async def get_general_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = get_general_session_maker()
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

session_maker = get_general_session_maker()

