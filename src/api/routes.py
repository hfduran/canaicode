from datetime import datetime
import io
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from src.config.config import CONFIG
from src.consumers.gh_copilot.gh_copilot_consumer import GhCopilotConsumer
from src.consumers.git_metrics_csv.git_metrics_csv_consumer import GitCommitMetricsCsvConsumer
from src.consumers.git_repo_consumer import GitRepoConsumer
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.use_cases.dtos.calculated_metrics import CalculatedMetrics, CopilotMetricsByLanguage, CopilotMetricsByPeriod, CopilotUsersMetrics
from src.domain.use_cases.get_calculated_metrics_use_case import GetCalculatedMetricsUseCase
from src.domain.use_cases.get_commit_metrics_use_case import GetCommitMetricsUseCase
from src.domain.use_cases.get_copilot_metrics_by_language_use_case import GetCopilotMetricsByLanguageUseCase
from src.domain.use_cases.get_copilot_metrics_by_period_use_case import GetCopilotMetricsByPeriodUseCase
from src.domain.use_cases.get_copilot_metrics_use_case import GetCopilotMetricsUseCase
from src.domain.use_cases.get_copilot_users_metrics_use_case import GetCopilotUsersMetricsUseCase
from src.domain.use_cases.get_csv_commit_metrics_use_case import GetCsvCommitMetricsUseCase
from src.infrastructure.database.connection.database_connection import SessionLocal
from src.infrastructure.database.raw_commit_metrics.postgre.raw_commit_metrics_repository import RawCommitMetricsRepository
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.raw_copilot_chat_metrics_repository import RawCopilotChatMetricsRepository
from src.infrastructure.database.raw_copilot_code_metrics.postgre.raw_copilot_code_metrics_repository import RawCopilotCodeMetricsRepository

router = APIRouter()


def get_db() -> Any:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/commit_metrics/upload/{team_name}")
def get_commit_metrics(
    team_name: str,
    date_string: str = "",
    db: Session = Depends(get_db),
) -> List[CommitMetrics]:
    date = datetime.strptime(date_string, "%Y-%m-%d").date()
    get_commit_metrics_use_case = set_get_commit_metrics_dependencies(db)
    response = get_commit_metrics_use_case.execute(date, team_name)
    return response


@router.get("/copilot_metrics/upload/{team_name}")
def get_copilot_metrics(
    team_name: str,
    date_string: str = "",
    db: Session = Depends(get_db),
) -> Dict[str, List[Any]]:
    date = datetime.strptime(date_string, "%Y-%m-%d").date()
    get_copilot_metrics_use_case = set_get_copilot_metrics_dependencies(db)
    response = get_copilot_metrics_use_case.execute(date, team_name)
    return response


@router.post("/commit_metrics/upload_csv")
def get_commit_metrics_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> List[CommitMetrics]:
    file_content = io.TextIOWrapper(file.file, encoding="utf-8")
    get_csv_commit_metrics_use_case = set_get_csv_commit_metrics_dependencies(db)
    response = get_csv_commit_metrics_use_case.execute(file_content)
    return response


@router.get("/calculated_metrics/{team_name}")
def get_calculated_metrics(
    team_name: str,
    period: str = "",
    productivity_metric: str = "",
    initial_date_string: str = "",
    final_date_string: str = "",
    languages_string: str = "",
    db: Session = Depends(get_db),
) -> CalculatedMetrics | None:
    initial_date = datetime.strptime(initial_date_string, "%Y-%m-%d")
    final_date = datetime.strptime(final_date_string, "%Y-%m-%d")
    languages: List[str] = []
    if(languages_string):
        languages = languages_string.split(',')
    get_calculated_metrics_use_case = set_get_calculated_metrics_dependencies(db)
    response = get_calculated_metrics_use_case.execute(team_name, period, productivity_metric, initial_date, final_date, languages) # type: ignore
    return response


@router.get("/copilot_metrics/language")
def get_copilot_metrics_by_language(
    initial_date_string: str = "",
    final_date_string: str = "",
    db: Session = Depends(get_db),
) -> List[CopilotMetricsByLanguage]:
    initial_date = None
    final_date = None
    if(initial_date_string):
        initial_date = datetime.strptime(initial_date_string, "%Y-%m-%d")
    if(final_date_string):
        final_date = datetime.strptime(final_date_string, "%Y-%m-%d")
    get_copilot_metrics_by_language_use_case = set_get_copilot_metrics_by_language_dependencies(db)
    response = get_copilot_metrics_by_language_use_case.execute(initial_date, final_date)
    return response

@router.get("/copilot_metrics/period")
def get_copilot_metrics_by_period(
    period: str = "",
    db: Session = Depends(get_db),
) -> List[CopilotMetricsByPeriod]:
    get_copilot_metrics_by_period_use_case = set_get_copilot_metrics_by_period_dependencies(db)
    response = get_copilot_metrics_by_period_use_case.execute(period) # type: ignore
    return response


@router.get("/copilot_metrics/users")
def get_copilot_metrics_by_users(
    db: Session = Depends(get_db),
) -> List[CopilotUsersMetrics]:
    get_copilot_users_metrics_use_case = set_get_copilot_users_metrics_dependencies(db)
    response = get_copilot_users_metrics_use_case.execute()
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


def set_get_csv_commit_metrics_dependencies(
    db: Session,
) -> GetCsvCommitMetricsUseCase:
    commit_metrics_repository = RawCommitMetricsRepository(db)
    git_commit_metrics_csv_consumer = GitCommitMetricsCsvConsumer()
    return GetCsvCommitMetricsUseCase(commit_metrics_repository, git_commit_metrics_csv_consumer)


def set_get_calculated_metrics_dependencies(
    db: Session,
) -> GetCalculatedMetricsUseCase:
    commit_metrics_repository = RawCommitMetricsRepository(db)
    copilot_code_metrics_repository = RawCopilotCodeMetricsRepository(db)
    return GetCalculatedMetricsUseCase(
        commit_metrics_repository,
        copilot_code_metrics_repository,
    )


def set_get_copilot_metrics_by_language_dependencies(
    db: Session,
) -> GetCopilotMetricsByLanguageUseCase:
    copilot_code_metrics_repository = RawCopilotCodeMetricsRepository(db)
    return GetCopilotMetricsByLanguageUseCase(
        copilot_code_metrics_repository,
    )


def set_get_copilot_metrics_by_period_dependencies(
    db: Session,
) -> GetCopilotMetricsByPeriodUseCase:
    copilot_code_metrics_repository = RawCopilotCodeMetricsRepository(db)
    return GetCopilotMetricsByPeriodUseCase(
        copilot_code_metrics_repository,
    )


def set_get_copilot_users_metrics_dependencies(
    db: Session,
) -> GetCopilotUsersMetricsUseCase:
    copilot_code_metrics_repository = RawCopilotCodeMetricsRepository(db)
    copilot_chat_metrics_repository = RawCopilotChatMetricsRepository(db)
    return GetCopilotUsersMetricsUseCase(
        copilot_code_metrics_repository,
        copilot_chat_metrics_repository,
    )
