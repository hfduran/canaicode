from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.infrastructure.database.postgre.raw_copilot_code_metrics.dtos.model import (
    RawCopilotCodeMetrics,
)
from src.infrastructure.database.postgre.raw_copilot_code_metrics.mappers.database_raw_copilot_code_metrics import (
    DatabaseRawCopilotCodeMetricsMapper,
)


class RawCopilotCodeMetricsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, copilot_code_metrics: CopilotCodeMetrics) -> None:
        record_to_save = DatabaseRawCopilotCodeMetricsMapper.to_database(
            copilot_code_metrics
        )

        self.db.add(record_to_save)
        self.db.commit()

    def listByTeam(
        self,
        team: str,
        initial_date: Optional[datetime] = None,
        final_date: Optional[datetime] = None,
        languages: Optional[List[str]] = None,
    ) -> List[CopilotCodeMetrics]:
        query = self.db.query(RawCopilotCodeMetrics)

        if initial_date:
            query = query.filter(RawCopilotCodeMetrics.date >= initial_date)

        if final_date:
            query = query.filter(RawCopilotCodeMetrics.date >= final_date)

        if languages:
            query = query.filter(RawCopilotCodeMetrics.language.in_(languages))

        records = query.filter(RawCopilotCodeMetrics.team_name == team).all()

        copilot_code_metrics = map(
            lambda record: DatabaseRawCopilotCodeMetricsMapper.to_domain(record),
            records,
        )

        return list(copilot_code_metrics)
