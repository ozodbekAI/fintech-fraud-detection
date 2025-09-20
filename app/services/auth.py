from fastapi import HTTPException
from sqlalchemy import select
from app.core.security import SecurityManager
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Token
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings

security = SecurityManager(secret_key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

class AuthService:

    async def register_user(user_data: UserCreate, db: AsyncSession) -> UserRead:
        existing_user = await db.execute(select(User).filter(User.email == user_data.email))
        if existing_user.scalars().first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = security.hash_password(password=user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=True,
            balance=0.0
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return UserRead.from_orm(new_user)
    
    async def login_user(email: str, password: str, db: AsyncSession) -> Token:
        result = await db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        if not user or not security.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        access_token = security.create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token)
    
    async def authenticate_user(token: str, db: AsyncSession) -> UserRead:
        try:
            payload = security.decode_access_token(token)
            user_id = int(payload.get("sub"))
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
        
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserRead.from_orm(user)