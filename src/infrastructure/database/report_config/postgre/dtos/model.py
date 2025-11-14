from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from src.infrastructure.database.connection.database_connection import Base


class ReportConfigDbSchema(Base):
  __tablename__ = "report_config"

  id = Column(String, primary_key=True, index=True)
  emails = Column(String)
  period = Column(String)
  user_id = Column(String, index=True)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
