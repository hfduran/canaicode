from sqlalchemy.orm import Session

from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
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
