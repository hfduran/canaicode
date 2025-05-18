from sqlalchemy.orm import Session

from src.domain.entities.commit_metrics import CommitMetrics
from src.infrastructure.database.postgre.raw_commit_metrics.mappers.database_raw_commit_metrics import (
    DatabaseRawCommitMetricsMapper,
)


class RawCommitMetricsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, commit_metrics: CommitMetrics) -> None:
        record_to_save = DatabaseRawCommitMetricsMapper.to_database(commit_metrics)

        self.db.add(record_to_save)
        self.db.commit()
