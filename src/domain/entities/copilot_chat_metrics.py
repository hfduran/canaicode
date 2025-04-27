from src.domain.entities.copilot_metrics import CopilotMetrics


class CopilotChatMetrics(CopilotMetrics):
    total_users: int
    total_chats: int
    copy_events: int
    insertion_events: int
