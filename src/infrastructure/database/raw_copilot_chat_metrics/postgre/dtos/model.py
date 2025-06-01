from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from src.infrastructure.database.connection.database_connection import Base

class RawCopilotChatMetrics(Base):
    __tablename__ = "raw_copilot_chat_metrics"

    id = Column(String, primary_key=True, index=True)
    team_name = Column(String, index=True)
    date = Column(DateTime, index=True)
    ide = Column(String)
    copilot_model = Column(String)
    total_users = Column(Integer)
    total_chats = Column(Integer)
    copy_events = Column(Integer)
    insertion_events = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
