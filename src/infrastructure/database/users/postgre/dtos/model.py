from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, UniqueConstraint
from src.infrastructure.database.connection.database_connection import Base


class UserDbSchema(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('username', name='users_username_key'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('cpf_cnpj', name='users_cpf_cnpj_key'),
    )

    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    full_name = Column(String(255))
    enterprise_name = Column(String(255), nullable=True)
    email = Column(String(255), index=True)
    cellphone = Column(String(20))
    cpf_cnpj = Column(String(18), index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))