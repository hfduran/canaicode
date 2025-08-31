from typing import Dict, List

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
        self, file_content: bytes, user_id: str
    ) -> Dict[str, List[CopilotCodeMetrics | CopilotChatMetrics]]:
        copilot_metrics = self.github_copilot_consumer.get_metrics(
            file_content, user_id
        )

        for copilot_code_metrics in copilot_metrics["code"]:
            if isinstance(copilot_code_metrics, CopilotCodeMetrics):
                self.copilot_code_metrics_repository.create(copilot_code_metrics)

        for copilot_chat_metrics in copilot_metrics["chat"]:
            if isinstance(copilot_chat_metrics, CopilotChatMetrics):
                self.copilot_chat_metrics_repository.create(copilot_chat_metrics)

        return copilot_metrics
