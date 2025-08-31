from typing import Optional, cast
from src.domain.entities.user import User
from src.infrastructure.database.users.postgre.dtos.model import UserDbSchema


class DatabaseUsersMapper:
    @staticmethod
    def to_database(user: User) -> UserDbSchema:
        return UserDbSchema(
            id=user.id,
            username=user.username,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
        )
    
    @staticmethod
    def to_domain(db_schema: UserDbSchema) -> User:
        return User(
            id=cast(Optional[str], db_schema.id),
            username=cast(str, db_schema.username),
            hashed_password=cast(str, db_schema.hashed_password),
        )
