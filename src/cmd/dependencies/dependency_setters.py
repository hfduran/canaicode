import os
from src.config.config import CONFIG
from src.consumers.gh_copilot.gh_copilot_consumer import GhCopilotConsumer
from src.consumers.git_metrics_xlsx.git_metrics_xlsx_consumer import GitCommitMetricsXlsxConsumer
from src.consumers.git_repo_consumer import GitRepoConsumer
from src.domain.use_cases.create_github_app_use_case import CreateGitHubAppUseCase
from src.domain.use_cases.create_user_use_case import CreateUserUseCase
from src.domain.use_cases.get_calculated_metrics_use_case import GetCalculatedMetricsUseCase
from src.domain.use_cases.get_commit_metrics_use_case import GetCommitMetricsUseCase
from src.domain.use_cases.get_copilot_metrics_by_language_use_case import GetCopilotMetricsByLanguageUseCase
from src.domain.use_cases.get_copilot_metrics_by_period_use_case import GetCopilotMetricsByPeriodUseCase
from src.domain.use_cases.get_copilot_metrics_use_case import GetCopilotMetricsUseCase
from src.domain.use_cases.get_copilot_users_metrics_use_case import GetCopilotUsersMetricsUseCase
from src.domain.use_cases.get_csv_commit_metrics_use_case import GetXlsxCommitMetricsUseCase
from src.domain.use_cases.validate_user_use_case import ValidateUserUseCase
from src.domain.use_cases.validate_api_key_use_case import ValidateApiKeyUseCase
from src.domain.use_cases.create_api_key_use_case import CreateApiKeyUseCase
from src.domain.use_cases.list_api_keys_use_case import ListApiKeysUseCase
from src.domain.use_cases.revoke_api_key_use_case import RevokeApiKeyUseCase
from src.infrastructure.database.api_keys.postgre.api_keys_repository import ApiKeysRepository
from src.infrastructure.database.github_apps.postgre.github_apps_repository import GitHubAppsRepository
from src.infrastructure.database.raw_commit_metrics.postgre.raw_commit_metrics_repository import RawCommitMetricsRepository
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.raw_copilot_chat_metrics_repository import RawCopilotChatMetricsRepository
from src.infrastructure.database.raw_copilot_code_metrics.postgre.raw_copilot_code_metrics_repository import RawCopilotCodeMetricsRepository
from src.infrastructure.database.users.postgre.users_repository import UsersRepository


from sqlalchemy.orm import Session

FERNET_KEY = os.getenv("FERNET_KEY")

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


def set_get_xlsx_commit_metrics_dependencies(
    db: Session,
) -> GetXlsxCommitMetricsUseCase:
    commit_metrics_repository = RawCommitMetricsRepository(db)
    git_commit_metrics_xlsx_consumer = GitCommitMetricsXlsxConsumer()
    return GetXlsxCommitMetricsUseCase(commit_metrics_repository, git_commit_metrics_xlsx_consumer)


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


def set_create_github_app_dependencies(
    db: Session
) -> CreateGitHubAppUseCase:
    github_apps_repository = GitHubAppsRepository(db)
    return CreateGitHubAppUseCase(github_apps_repository, encryption_key=FERNET_KEY) # type: ignore


def set_validate_api_key_dependencies(
    db: Session,
) -> ValidateApiKeyUseCase:
    api_keys_repository = ApiKeysRepository(db)
    return ValidateApiKeyUseCase(api_keys_repository)


def set_create_api_key_dependencies(
    db: Session,
) -> CreateApiKeyUseCase:
    api_keys_repository = ApiKeysRepository(db)
    return CreateApiKeyUseCase(api_keys_repository)


def set_list_api_keys_dependencies(
    db: Session,
) -> ListApiKeysUseCase:
    api_keys_repository = ApiKeysRepository(db)
    return ListApiKeysUseCase(api_keys_repository)


def set_revoke_api_key_dependencies(
    db: Session,
) -> RevokeApiKeyUseCase:
    api_keys_repository = ApiKeysRepository(db)
    return RevokeApiKeyUseCase(api_keys_repository)