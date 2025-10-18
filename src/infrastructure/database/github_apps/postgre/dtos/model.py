from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from src.infrastructure.database.connection.database_connection import Base


class GitHubAppDbSchema(Base):
  __tablename__ = "github_apps"

  id = Column(String, primary_key=True, index=True)
  organization_name = Column(String)
  app_id = Column(String)
  installation_id = Column(String)
  private_key_encrypted = Column(String)
  user_id = Column(String, index=True)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
