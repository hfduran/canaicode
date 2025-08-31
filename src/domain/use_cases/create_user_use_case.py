import uuid
from fastapi import HTTPException

from src.domain.entities.user import User
from src.infrastructure.database.users.postgre.users_repository import UsersRepository
from passlib.context import CryptContext

class CreateUserUseCase:
    def __init__(
        self,
        users_repository: UsersRepository,
    ) -> None:
        self.users_repository = users_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def execute(self, username: str, password: str) -> User:
        persisted_user = self.users_repository.find_by_username(username)
        if persisted_user:
          raise HTTPException(status_code=400, detail="This username already exists")

        hashed_password = self.get_password_hash(password)
        new_user = User(id=str(uuid.uuid4()), username=username, hashed_password=hashed_password)
        self.users_repository.create(new_user)
        return new_user
    

    def get_password_hash(self, password: str) -> str:
      return self.pwd_context.hash(password) # type: ignore
