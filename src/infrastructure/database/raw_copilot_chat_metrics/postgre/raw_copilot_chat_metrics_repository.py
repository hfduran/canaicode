from typing import List
from sqlalchemy.orm import Session

from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.dtos.model import RawCopilotChatMetrics
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.mappers.database_raw_copilot_chat_metrics import DatabaseRawCopilotChatMetricsMapper

class RawCopilotChatMetricsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, copilot_chat_metrics: CopilotChatMetrics) -> None:
        record_to_save = DatabaseRawCopilotChatMetricsMapper.to_database(
            copilot_chat_metrics
        )

        self.db.add(record_to_save)
        self.db.commit()

    def listByUserId(
        self,
        user_id: str
    ) -> List[CopilotChatMetrics]:
        query = self.db.query(RawCopilotChatMetrics)

        records = query.filter(RawCopilotChatMetrics.user_id == user_id).all()

        copilot_chat_metrics = map(
            lambda record: DatabaseRawCopilotChatMetricsMapper.to_domain(record),
            records,
        )

        return list(copilot_chat_metrics)
