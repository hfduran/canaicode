from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter

from src.config.config import CONFIG
from src.consumers.gh_copilot.gh_copilot_consumer import GhCopilotConsumer
from src.consumers.git_repo_consumer import GitRepoConsumer
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.use_cases.get_commit_metrics_use_case import GetCommitMetricsUseCase
from src.domain.use_cases.get_copilot_metrics_use_case import GetCopilotMetricsUseCase
from src.infrastructure.database.dynamo.raw_commit_metrics_repository import (
    RawCommitMetricsRepository,
)
from src.infrastructure.database.dynamo.raw_copilot_chat_metrics_repository import (
    RawCopilotChatMetricsRepository,
)
from src.infrastructure.database.dynamo.raw_copilot_code_metrics_repository import (
    RawCopilotCodeMetricsRepository,
)

router = APIRouter()


@router.get("/commit_metrics")
def get_commit_metrics(date_string: str = "") -> List[CommitMetrics]:
    date = datetime.strptime(date_string, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    get_commit_metrics_use_case = set_get_commit_metrics_dependencies()
    response = get_commit_metrics_use_case.execute(date)
    return response


@router.get("/copilot_metrics")
def get_copilot_metrics(
    date_string: str = "",
) -> Dict[str, List[Any]]:
    date = datetime.strptime(date_string, "%Y-%m-%d").date()
    get_copilot_metrics_use_case = set_get_copilot_metrics_dependencies()
    response = get_copilot_metrics_use_case.execute(date)
    return response


def set_get_commit_metrics_dependencies() -> GetCommitMetricsUseCase:
    commit_metrics_repository = RawCommitMetricsRepository()
    git_repo_consumer = GitRepoConsumer(CONFIG.repo_path)
    return GetCommitMetricsUseCase(commit_metrics_repository, git_repo_consumer)


def set_get_copilot_metrics_dependencies() -> GetCopilotMetricsUseCase:
    copilot_code_metrics_repository = RawCopilotCodeMetricsRepository()
    copilot_chat_metrics_repository = RawCopilotChatMetricsRepository()
    github_copilot_consumer = GhCopilotConsumer()
    return GetCopilotMetricsUseCase(
        copilot_code_metrics_repository,
        copilot_chat_metrics_repository,
        github_copilot_consumer,
    )
