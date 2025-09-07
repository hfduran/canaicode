from datetime import datetime, timedelta
import os
from jose import jwt
from fastapi import HTTPException

from src.domain.use_cases.dtos.token import Token
from src.infrastructure.database.users.postgre.users_repository import UsersRepository
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60

class ValidateUserUseCase:
    def __init__(
        self,
        users_repository: UsersRepository,
    ) -> None:
        self.users_repository = users_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def execute(self, username: str, password: str) -> Token:
        user = self.users_repository.find_by_username(username)
        if not user or not self.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = self.create_access_token({"sub": user.username, "user_id": user.id}) # type: ignore
        return Token(user_id=user.id, access_token=access_token, token_type="bearer") # type: ignore
    

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
      return self.pwd_context.verify(plain_password, hashed_password) # type: ignore
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str: # type: ignore
      to_encode = data.copy() # type: ignore
      expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))) # type: ignore
      to_encode.update({"exp": expire}) # type: ignore
      return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
