from sqlalchemy.orm import Session

from src.domain.entities.user import User
from src.infrastructure.database.users.postgre.dtos.model import UserDbSchema
from src.infrastructure.database.users.postgre.mappers.database_users import DatabaseUsersMapper

class UsersRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user: User) -> None:
        record_to_save = DatabaseUsersMapper.to_database(
            user
        )

        self.db.add(record_to_save)
        self.db.commit()

    def find_by_username(
        self,
        username: str
    ) -> User | None:
        query = self.db.query(UserDbSchema)

        record = query.filter(UserDbSchema.username == username).first()

        if(not record):
            return None

        return DatabaseUsersMapper.to_domain(record)

    def find_by_id(
        self,
        user_id: str
    ) -> User | None:
        query = self.db.query(UserDbSchema)

        record = query.filter(UserDbSchema.id == user_id).first()

        if(not record):
            return None

        return DatabaseUsersMapper.to_domain(record)

    def find_by_email(
        self,
        email: str
    ) -> User | None:
        query = self.db.query(UserDbSchema)

        record = query.filter(UserDbSchema.email == email).first()

        if(not record):
            return None

        return DatabaseUsersMapper.to_domain(record)

    def find_by_cpf_cnpj(
        self,
        cpf_cnpj: str
    ) -> User | None:
        query = self.db.query(UserDbSchema)

        record = query.filter(UserDbSchema.cpf_cnpj == cpf_cnpj).first()

        if(not record):
            return None

        return DatabaseUsersMapper.to_domain(record)
