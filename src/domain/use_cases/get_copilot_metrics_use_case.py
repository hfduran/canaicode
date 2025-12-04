from typing import Dict, List, Any

from src.consumers.gh_copilot.gh_copilot_consumer import GhCopilotConsumer
from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.raw_copilot_chat_metrics_repository import RawCopilotChatMetricsRepository
from src.infrastructure.database.raw_copilot_code_metrics.postgre.raw_copilot_code_metrics_repository import RawCopilotCodeMetricsRepository

class GetCopilotMetricsUseCase:
    def __init__(
        self,
        copilot_code_metrics_repository: RawCopilotCodeMetricsRepository,
        copilot_chat_metrics_repository: RawCopilotChatMetricsRepository,
        github_copilot_consumer: GhCopilotConsumer,
    ) -> None:
        self.copilot_code_metrics_repository = copilot_code_metrics_repository
        self.copilot_chat_metrics_repository = copilot_chat_metrics_repository
        self.github_copilot_consumer = github_copilot_consumer

    def execute(
        self, data: Dict[Any, Any], user_id: str
    ) -> Dict[str, List[CopilotCodeMetrics | CopilotChatMetrics]]:
        copilot_metrics = self.github_copilot_consumer.get_metrics(
            data, user_id
        )

        # Bulk upsert code metrics
        code_metrics_to_insert = [
            copilot_code_metrics
            for copilot_code_metrics in copilot_metrics["code"]
            if isinstance(copilot_code_metrics, CopilotCodeMetrics)
        ]
        if code_metrics_to_insert:
            self.copilot_code_metrics_repository.upsert_many(code_metrics_to_insert)

        # Bulk upsert chat metrics
        chat_metrics_to_insert = [
            copilot_chat_metrics
            for copilot_chat_metrics in copilot_metrics["chat"]
            if isinstance(copilot_chat_metrics, CopilotChatMetrics)
        ]
        if chat_metrics_to_insert:
            self.copilot_chat_metrics_repository.upsert_many(chat_metrics_to_insert)

        return copilot_metrics
