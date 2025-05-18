from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.infrastructure.database.postgre.raw_copilot_code_metrics.dtos.model import (
    RawCopilotCodeMetrics,
)


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
        )
