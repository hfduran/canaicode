from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from src.infrastructure.database.connection.database_connection import Base


class ApiKeyDbSchema(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    key_name = Column(String(255))
    key_hash = Column(String)
    key_prefix = Column(String(20))  # For display: "cak_abc...xyz"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
