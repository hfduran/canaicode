from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.entities.commit_metrics import CommitMetrics
from src.infrastructure.database.raw_commit_metrics.postgre.dtos.model import RawCommitMetrics
from src.infrastructure.database.raw_commit_metrics.postgre.mappers.database_raw_commit_metrics import DatabaseRawCommitMetricsMapper


class RawCommitMetricsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, commit_metrics: CommitMetrics) -> None:
        record_to_save = DatabaseRawCommitMetricsMapper.to_database(commit_metrics)

        self.db.add(record_to_save)
        self.db.commit()

    def listByTeam(
        self,
        team: str,
        initial_date: Optional[datetime] = None,
        final_date: Optional[datetime] = None,
        languages: Optional[List[str]] = None,
    ) -> List[CommitMetrics]:
        query = self.db.query(RawCommitMetrics)

        if initial_date:
            query = query.filter(RawCommitMetrics.date >= initial_date)

        if final_date:
            query = query.filter(RawCommitMetrics.date <= final_date)

        if languages:
            query = query.filter(RawCommitMetrics.language.in_(languages))

        records = query.filter(RawCommitMetrics.repository_team == team).all()

        commit_metrics = map(
            lambda record: DatabaseRawCommitMetricsMapper.to_domain(record), records
        )

        return list(commit_metrics)
