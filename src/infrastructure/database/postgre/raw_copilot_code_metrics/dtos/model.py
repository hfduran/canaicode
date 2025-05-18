from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from src.infrastructure.database.postgre.connection.database_connection import Base


class RawCopilotCodeMetrics(Base):
    __tablename__ = "raw_copilot_code_metrics"

    id = Column(String, primary_key=True, index=True)
    team_name = Column(String, index=True)
    date = Column(DateTime, index=True)
    ide = Column(String)
    copilot_model = Column(String)
    language = Column(String)
    total_users = Column(Integer)
    code_acceptances = Column(Integer)
    code_suggestions = Column(Integer)
    lines_accepted = Column(Integer)
    lines_suggested = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
