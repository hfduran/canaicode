from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint

from src.infrastructure.database.connection.database_connection import Base



class RawCommitMetrics(Base):
    __tablename__ = "raw_commit_metrics"

    id = Column(String, primary_key=True, index=True)
    hash = Column(String)
    repository_name = Column(String)
    repository_team = Column(String, index=True)
    date = Column(DateTime, index=True)
    author_name = Column(String)
    author_teams = Column(String, index=True)
    language = Column(String)
    added_lines = Column(Integer)
    removed_lines = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(String, index=True)

    __table_args__ = (
        UniqueConstraint('user_id', 'hash', 'repository_name', 'language', name='unique_commit_per_repo_lang'),
    )
