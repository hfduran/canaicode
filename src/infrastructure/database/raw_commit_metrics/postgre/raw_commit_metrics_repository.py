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

    def create_many(self, commit_metrics_list: List[CommitMetrics]) -> None:
        records_to_save = [
            DatabaseRawCommitMetricsMapper.to_database(cm)
            for cm in commit_metrics_list
        ]

        self.db.add_all(records_to_save)
        self.db.commit()

    def listByUserId(
        self,
        user_id: str,
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

        records = query.filter(RawCommitMetrics.user_id == user_id).all()

        commit_metrics = map(
            lambda record: DatabaseRawCommitMetricsMapper.to_domain(record), records
        )

        return list(commit_metrics)
