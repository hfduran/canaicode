from fastapi import HTTPException
from src.infrastructure.database.raw_commit_metrics.postgre.raw_commit_metrics_repository import RawCommitMetricsRepository
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.raw_copilot_chat_metrics_repository import RawCopilotChatMetricsRepository
from src.infrastructure.database.raw_copilot_code_metrics.postgre.raw_copilot_code_metrics_repository import RawCopilotCodeMetricsRepository
from src.infrastructure.database.users.postgre.users_repository import UsersRepository


class DeleteMetricsUseCase:
    def __init__(
        self,
        users_repository: UsersRepository,
        commit_metrics_repository: RawCommitMetricsRepository,
        copilot_code_metrics_repository: RawCopilotCodeMetricsRepository,
        copilot_chat_metrics_repository: RawCopilotChatMetricsRepository,
    ) -> None:
        self.users_repository = users_repository
        self.commit_metrics_repository = commit_metrics_repository
        self.copilot_code_metrics_repository = copilot_code_metrics_repository
        self.copilot_chat_metrics_repository = copilot_chat_metrics_repository

    def execute(
        self,
        username: str,
    ) -> None:
        user = self.users_repository.find_by_username(username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        self.commit_metrics_repository.deleteByUserId(user.id)
        self.copilot_code_metrics_repository.deleteByUserId(user.id)
        self.copilot_chat_metrics_repository.deleteByUserId(user.id)