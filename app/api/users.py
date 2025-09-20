from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.core.database import get_general_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth import AuthService

security = HTTPBearer()

app = APIRouter(
    prefix="/auth",
    tags=["users"],
)


@app.post("/register/")
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_general_session),
):
    return await AuthService.register_user(user_data=user, db=db)

@app.post("/login/")
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_general_session),
):
    return await AuthService.login_user(email=user_data.email, password=user_data.password, db=db)


@app.get("/balance/")
async def get_balance(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_general_session),
):
    token = credentials.credentials
    user = await AuthService.authenticate_user(token=token, db=db)
    return {"balance": user.balance}


@app.post("/deposit/")
async def deposit(
    amount: float,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_general_session),
):
    token = credentials.credentials
    user = await AuthService.authenticate_user(token=token, db=db)
    user.balance += amount
    await db.commit()
    return {"balance": user.balance}