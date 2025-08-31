from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, UniqueConstraint
from src.infrastructure.database.connection.database_connection import Base


class UserDbSchema(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('username', name='users_username_key'),
    )

    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))