from datetime import datetime
from typing import Optional, cast

from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.domain.entities.value_objects.team import Team
from src.infrastructure.database.raw_copilot_code_metrics.postgre.dtos.model import RawCopilotCodeMetrics

class DatabaseRawCopilotCodeMetricsMapper:
    @staticmethod
    def to_database(copilot_code_metrics: CopilotCodeMetrics) -> RawCopilotCodeMetrics:
        return RawCopilotCodeMetrics(
            id=copilot_code_metrics.id,
            team_name=copilot_code_metrics.team.name,
            date=copilot_code_metrics.date,
            ide=copilot_code_metrics.IDE,
            copilot_model=copilot_code_metrics.copilot_model,
            language=copilot_code_metrics.language,
            total_users=copilot_code_metrics.total_users,
            code_acceptances=copilot_code_metrics.code_acceptances,
            code_suggestions=copilot_code_metrics.code_suggestions,
            lines_accepted=copilot_code_metrics.lines_accepted,
            lines_suggested=copilot_code_metrics.lines_suggested,
            created_at=copilot_code_metrics.created_at,
            user_id=copilot_code_metrics.user_id
        )

    @staticmethod
    def to_domain(db_schema: RawCopilotCodeMetrics) -> CopilotCodeMetrics:
        team = Team(name=cast(str, db_schema.team_name))

        return CopilotCodeMetrics(
            id=cast(str, db_schema.id),
            team=team,
            date=cast(datetime, db_schema.date),
            IDE=cast(str, db_schema.ide),
            copilot_model=cast(str, db_schema.copilot_model),
            created_at=cast(Optional[datetime], db_schema.created_at),
            language=cast(str, db_schema.language),
            total_users=cast(int, db_schema.total_users),
            code_acceptances=cast(int, db_schema.code_acceptances),
            code_suggestions=cast(int, db_schema.code_suggestions),
            lines_accepted=cast(int, db_schema.lines_accepted),
            lines_suggested=cast(int, db_schema.lines_suggested),
            user_id=cast(str, db_schema.user_id)
        )
