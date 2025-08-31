from datetime import datetime
import io
import os
from typing import Any, Dict, List
from jose import JWTError, jwt

from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.config.config import CONFIG
from src.consumers.gh_copilot.gh_copilot_consumer import GhCopilotConsumer
from src.consumers.git_metrics_csv.git_metrics_csv_consumer import GitCommitMetricsCsvConsumer
from src.consumers.git_repo_consumer import GitRepoConsumer
from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.user import User
from src.domain.use_cases.create_user_use_case import CreateUserUseCase
from src.domain.use_cases.dtos.calculated_metrics import CalculatedMetrics, CopilotMetricsByLanguage, CopilotMetricsByPeriod, CopilotUsersMetrics
from src.domain.use_cases.dtos.token import Token
from src.domain.use_cases.get_calculated_metrics_use_case import GetCalculatedMetricsUseCase
from src.domain.use_cases.get_commit_metrics_use_case import GetCommitMetricsUseCase
from src.domain.use_cases.get_copilot_metrics_by_language_use_case import GetCopilotMetricsByLanguageUseCase
from src.domain.use_cases.get_copilot_metrics_by_period_use_case import GetCopilotMetricsByPeriodUseCase
from src.domain.use_cases.get_copilot_metrics_use_case import GetCopilotMetricsUseCase
from src.domain.use_cases.get_copilot_users_metrics_use_case import GetCopilotUsersMetricsUseCase
from src.domain.use_cases.get_csv_commit_metrics_use_case import GetCsvCommitMetricsUseCase
from src.domain.use_cases.validate_user_use_case import ValidateUserUseCase
from src.infrastructure.database.connection.database_connection import SessionLocal
from src.infrastructure.database.raw_commit_metrics.postgre.raw_commit_metrics_repository import RawCommitMetricsRepository
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.raw_copilot_chat_metrics_repository import RawCopilotChatMetricsRepository
from src.infrastructure.database.raw_copilot_code_metrics.postgre.raw_copilot_code_metrics_repository import RawCopilotCodeMetricsRepository
from src.infrastructure.database.users.postgre.users_repository import UsersRepository

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db() -> Any:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=User)
def register(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    db: Session = Depends(get_db)
)-> User:
    create_user_use_case = set_create_user_dependencies(db)
    response = create_user_use_case.execute(username, password)
    return response


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    validate_user_use_case = set_validate_user_dependencies(db)
    response = validate_user_use_case.execute(form_data.username, form_data.password)
    return response


@router.get("/commit_metrics/upload_deprecated/{team_name}")
def get_commit_metrics(
    team_name: str,
    user_id: str = "",
    date_string: str = "",
    db: Session = Depends(get_db),
) -> List[CommitMetrics]:
    date = datetime.strptime(date_string, "%Y-%m-%d").date()
    get_commit_metrics_use_case = set_get_commit_metrics_dependencies(db)
    response = get_commit_metrics_use_case.execute(date, team_name, user_id)
    return response


@router.post("/copilot_metrics/upload")
async def get_copilot_metrics(
    file: UploadFile = File(...),
    user_id: str = Body(..., embed=True),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Dict[str, List[Any]]:
    validate_token(token)
    file_content = await file.read()
    get_copilot_metrics_use_case = set_get_copilot_metrics_dependencies(db)
    response = get_copilot_metrics_use_case.execute(file_content, user_id)
    return response


@router.post("/commit_metrics/upload")
def get_commit_metrics_csv(
    file: UploadFile = File(...),
    user_id: str = Body(..., embed=True),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> List[CommitMetrics]:
    validate_token(token)
    file_content = io.TextIOWrapper(file.file, encoding="utf-8")
    get_csv_commit_metrics_use_case = set_get_csv_commit_metrics_dependencies(db)
    response = get_csv_commit_metrics_use_case.execute(file_content, user_id)
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


def validate_token(token: str) -> str | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")


def set_create_user_dependencies(
    db: Session,
) -> CreateUserUseCase:
    users_repository = UsersRepository(db)
    return CreateUserUseCase(users_repository)


def set_validate_user_dependencies(
    db: Session,
) -> ValidateUserUseCase:
    users_repository = UsersRepository(db)
    return ValidateUserUseCase(users_repository)


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
