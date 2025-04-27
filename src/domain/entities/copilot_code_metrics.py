from src.domain.entities.copilot_metrics import CopilotMetrics


class CopilotCodeMetrics(CopilotMetrics):
    language: str
    total_users: int
    code_acceptances: int
    code_suggestions: int
    lines_accepted: int
    lines_suggested: int
