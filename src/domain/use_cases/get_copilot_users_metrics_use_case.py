from datetime import datetime
from typing import DefaultDict, Dict, List
from src.domain.use_cases.dtos.calculated_metrics import CopilotUsersMetrics
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.raw_copilot_chat_metrics_repository import RawCopilotChatMetricsRepository
from src.infrastructure.database.raw_copilot_code_metrics.postgre.raw_copilot_code_metrics_repository import RawCopilotCodeMetricsRepository


class GetCopilotUsersMetricsUseCase:
  def __init__(
        self,
        copilot_code_metrics_repository: RawCopilotCodeMetricsRepository,
        copilot_chat_metrics_repository: RawCopilotChatMetricsRepository,
    ) -> None:
        self.copilot_code_metrics_repository = copilot_code_metrics_repository
        self.copilot_chat_metrics_repository = copilot_chat_metrics_repository

  def execute(self) -> List[CopilotUsersMetrics]:
    raw_copilot_code_metrics = self.copilot_code_metrics_repository.list()

    if (not raw_copilot_code_metrics):
      return []
    
    grouped_code_metrics: DefaultDict[datetime, Dict[str, int]] = DefaultDict(lambda: {
      "total_users": 0,
    })

    for metric in raw_copilot_code_metrics:
      date = metric.date
      grouped_code_metrics[date]["total_users"] += metric.total_users

    response: List[CopilotUsersMetrics] = []
    for date_code_metrics, values_code_metrics in grouped_code_metrics.items():
        response.append(CopilotUsersMetrics(
            date=date_code_metrics,
            total_code_assistant_users=values_code_metrics["total_users"],
            total_chat_users=0
        ))

    raw_copilot_chat_metrics = self.copilot_chat_metrics_repository.list()

    grouped_chat_metrics: DefaultDict[datetime, Dict[str, int]] = DefaultDict(lambda: {
      "total_users": 0,
    })

    for chat_metric in raw_copilot_chat_metrics:
      date = chat_metric.date
      grouped_chat_metrics[date]["total_users"] += chat_metric.total_users

    for date_chat_metrics, values_chat_metrics in grouped_chat_metrics.items():
        index = next(
            i
            for i, data in enumerate(response)
            if data.date == date_chat_metrics
        )
        response[index].total_chat_users = values_chat_metrics["total_users"]

    return response