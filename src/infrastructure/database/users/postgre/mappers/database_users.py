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
            full_name=user.full_name,
            enterprise_name=user.enterprise_name,
            email=user.email,
            cellphone=user.cellphone,
            cpf_cnpj=user.cpf_cnpj,
            created_at=user.created_at,
        )

    @staticmethod
    def to_domain(db_schema: UserDbSchema) -> User:
        return User(
            id=cast(Optional[str], db_schema.id),
            username=cast(str, db_schema.username),
            hashed_password=cast(str, db_schema.hashed_password),
            full_name=cast(str, db_schema.full_name),
            enterprise_name=cast(Optional[str], db_schema.enterprise_name),
            email=cast(str, db_schema.email),
            cellphone=cast(str, db_schema.cellphone),
            cpf_cnpj=cast(str, db_schema.cpf_cnpj),
        )
