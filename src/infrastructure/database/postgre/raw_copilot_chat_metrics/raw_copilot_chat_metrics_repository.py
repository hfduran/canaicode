from sqlalchemy.orm import Session

from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.infrastructure.database.postgre.raw_copilot_chat_metrics.mappers.database_raw_copilot_chat_metrics import (
    DatabaseRawCopilotChatMetricsMapper,
)


class RawCopilotChatMetricsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, copilot_chat_metrics: CopilotChatMetrics) -> None:
        record_to_save = DatabaseRawCopilotChatMetricsMapper.to_database(
            copilot_chat_metrics
        )

        self.db.add(record_to_save)
        self.db.commit()
