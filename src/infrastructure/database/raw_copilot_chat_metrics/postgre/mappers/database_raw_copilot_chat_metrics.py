from datetime import datetime
from typing import Optional, cast
from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.domain.entities.value_objects.team import Team
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
            user_id=copilot_chat_metrics.user_id
        )
    
    @staticmethod
    def to_domain(db_schema: RawCopilotChatMetrics) -> CopilotChatMetrics:
        team = Team(name=cast(str, db_schema.team_name))

        return CopilotChatMetrics(
            id=cast(Optional[str], db_schema.id),
            team=team,
            date=cast(datetime, db_schema.date),
            IDE=cast(str, db_schema.ide),
            copilot_model=cast(str, db_schema.copilot_model),
            created_at=cast(Optional[datetime], db_schema.created_at),
            total_users=cast(int, db_schema.total_users),
            total_chats=cast(int, db_schema.total_chats),
            copy_events=cast(int, db_schema.copy_events),
            insertion_events=cast(int, db_schema.insertion_events),
            user_id=cast(str, db_schema.user_id)
        )
