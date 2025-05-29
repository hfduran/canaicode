from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.dtos.model import RawCopilotChatMetrics


class DatabaseRawCopilotChatMetricsMapper:
    @staticmethod
    def to_database(copilot_chat_metrics: CopilotChatMetrics) -> RawCopilotChatMetrics:
        return RawCopilotChatMetrics(
            id=copilot_chat_metrics.id,
            team_name=copilot_chat_metrics.team.name,
            date=copilot_chat_metrics.date,
            ide=copilot_chat_metrics.IDE,
            copilot_model=copilot_chat_metrics.copilot_model,
            total_users=copilot_chat_metrics.total_users,
            total_chats=copilot_chat_metrics.total_chats,
            copy_events=copilot_chat_metrics.copy_events,
            insertion_events=copilot_chat_metrics.insertion_events,
            created_at=copilot_chat_metrics.created_at,
        )
