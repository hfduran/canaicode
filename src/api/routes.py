from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.config import CONFIG
from src.consumers.gh_copilot.gh_copilot_consumer import GhCopilotConsumer
from src.consumers.git_repo_consumer import GitRepoConsumer
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.use_cases.get_commit_metrics_use_case import GetCommitMetricsUseCase
from src.domain.use_cases.get_copilot_metrics_use_case import GetCopilotMetricsUseCase
from src.infrastructure.database.postgre.connection.database_connection import (
    SessionLocal,
)
from src.infrastructure.database.postgre.raw_commit_metrics.raw_commit_metrics_repository import (
    RawCommitMetricsRepository,
)
from src.infrastructure.database.postgre.raw_copilot_chat_metrics.raw_copilot_chat_metrics_repository import (
    RawCopilotChatMetricsRepository,
)
from src.infrastructure.database.postgre.raw_copilot_code_metrics.raw_copilot_code_metrics_repository import (
    RawCopilotCodeMetricsRepository,
)

router = APIRouter()


def get_db() -> Any:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/commit_metrics/{team_name}")
def get_commit_metrics(
    team_name: str,
    date_string: str = "",
    db: Session = Depends(get_db),
) -> List[CommitMetrics]:
    date = datetime.strptime(date_string, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    get_commit_metrics_use_case = set_get_commit_metrics_dependencies(db)
    response = get_commit_metrics_use_case.execute(date, team_name)
    return response


@router.get("/copilot_metrics/{team_name}")
def get_copilot_metrics(
    team_name: str,
    date_string: str = "",
    db: Session = Depends(get_db),
) -> Dict[str, List[Any]]:
    date = datetime.strptime(date_string, "%Y-%m-%d").date()
    get_copilot_metrics_use_case = set_get_copilot_metrics_dependencies(db)
    response = get_copilot_metrics_use_case.execute(date, team_name)
    return response


def set_get_commit_metrics_dependencies(
    db: Session,
) -> GetCommitMetricsUseCase:
    commit_metrics_repository = RawCommitMetricsRepository(db)
    git_repo_consumer = GitRepoConsumer(CONFIG.repo_path)
    return GetCommitMetricsUseCase(commit_metrics_repository, git_repo_consumer)


def set_get_copilot_metrics_dependencies(
    db: Session,
) -> GetCopilotMetricsUseCase:
    copilot_code_metrics_repository = RawCopilotCodeMetricsRepository(db)
    copilot_chat_metrics_repository = RawCopilotChatMetricsRepository(db)
    github_copilot_consumer = GhCopilotConsumer()
    return GetCopilotMetricsUseCase(
        copilot_code_metrics_repository,
        copilot_chat_metrics_repository,
        github_copilot_consumer,
    )
