import datetime
from typing import Annotated
from passlib.context import CryptContext
import jwt

class SecurityManager():
    def __init__(
            self,
            secret_key: str,
            algorithm: str = "HS256",
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.crypt_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.crypt_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict, expires_delta: datetime.timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError("Invalid token")
        
    def refresh_access_token(self, token: str, expires_delta: datetime.timedelta | None = None) -> str:
        payload = self.decode_access_token(token)
        payload.pop("exp", None)  # Remove the old expiration
        return self.create_access_token(payload, expires_delta)
    
    