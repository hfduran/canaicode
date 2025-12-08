import os
from src.config.config import CONFIG
from src.consumers.gh_copilot.gh_copilot_consumer import GhCopilotConsumer
from src.consumers.git_metrics_xlsx.git_metrics_xlsx_consumer import GitCommitMetricsXlsxConsumer
from src.consumers.git_repo_consumer import GitRepoConsumer
from src.domain.use_cases.create_github_app_use_case import CreateGitHubAppUseCase
from src.domain.use_cases.create_report_config_use_case import CreateReportConfigUseCase
from src.domain.use_cases.create_user_use_case import CreateUserUseCase
from src.domain.use_cases.delete_github_app_use_case import DeleteGitHubAppUseCase
from src.domain.use_cases.delete_metrics_use_case import DeleteMetricsUseCase
from src.domain.use_cases.delete_report_config_use_case import DeleteReportConfigUseCase
from src.domain.use_cases.fetch_copilot_metrics_use_case import FetchCopilotMetricsUseCase
from src.domain.use_cases.find_github_app_use_case import FindGitHubAppUseCase
from src.domain.use_cases.find_report_config_use_case import FindReportConfigUseCase
from src.domain.use_cases.get_calculated_metrics_use_case import GetCalculatedMetricsUseCase
from src.domain.use_cases.get_commit_metrics_use_case import GetCommitMetricsUseCase
from src.domain.use_cases.get_copilot_metrics_by_language_use_case import GetCopilotMetricsByLanguageUseCase
from src.domain.use_cases.get_copilot_metrics_by_period_use_case import GetCopilotMetricsByPeriodUseCase
from src.domain.use_cases.get_copilot_metrics_use_case import GetCopilotMetricsUseCase
from src.domain.use_cases.get_copilot_users_metrics_use_case import GetCopilotUsersMetricsUseCase
from src.domain.use_cases.get_csv_commit_metrics_use_case import GetXlsxCommitMetricsUseCase
from src.domain.use_cases.send_metrics_email_use_case import SendMetricsEmailUseCase
from src.domain.use_cases.update_report_config_use_case import UpdateReportConfigUseCase
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
from src.infrastructure.database.report_config.postgre.report_config_repository import ReportConfigRepository
from src.infrastructure.database.users.postgre.users_repository import UsersRepository


from sqlalchemy.orm import Session

FERNET_KEY = os.getenv("FERNET_KEY")
MAIL_NAME = os.getenv("MAIL_NAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
UNSUBSCRIBE_LINK = os.getenv("UNSUBSCRIBE_LINK")

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

def set_fetch_copilot_metrics_dependencies(
    db: Session
) -> FetchCopilotMetricsUseCase:
    github_apps_repository = GitHubAppsRepository(db)
    get_copilot_metrics_use_case = set_get_copilot_metrics_dependencies(db)
    return FetchCopilotMetricsUseCase(github_apps_repository, get_copilot_metrics_use_case, encryption_key=FERNET_KEY) # type: ignore

def set_send_metrics_email_dependencies(
    db: Session
) -> SendMetricsEmailUseCase:
    report_config_repository = ReportConfigRepository(db)
    github_apps_repository = GitHubAppsRepository(db)
    get_calculated_metrics_use_case = set_get_calculated_metrics_dependencies(db)
    get_copilot_metrics_by_language_use_case = set_get_copilot_metrics_by_language_dependencies(db)
    get_copilot_metrics_by_period_use_case = set_get_copilot_metrics_by_period_dependencies(db)
    get_copilot_users_metrics_use_case = set_get_copilot_users_metrics_dependencies(db)
    return SendMetricsEmailUseCase(report_config_repository, github_apps_repository, get_calculated_metrics_use_case, get_copilot_metrics_by_language_use_case, get_copilot_metrics_by_period_use_case, get_copilot_users_metrics_use_case, mail_name=MAIL_NAME, mail_password=MAIL_PASSWORD, encryption_key=FERNET_KEY, unsubscribe_link=UNSUBSCRIBE_LINK) # type: ignore

def set_find_github_app_dependencies(
    db: Session
) -> FindGitHubAppUseCase:
    github_apps_repository = GitHubAppsRepository(db)
    return FindGitHubAppUseCase(github_apps_repository)

def set_delete_github_app_dependencies(
    db: Session
) -> DeleteGitHubAppUseCase:
    github_apps_repository = GitHubAppsRepository(db)
    return DeleteGitHubAppUseCase(github_apps_repository)

def set_create_report_config_dependencies(
    db: Session
) -> CreateReportConfigUseCase:
    report_config_repository = ReportConfigRepository(db)
    return CreateReportConfigUseCase(report_config_repository)

def set_find_report_config_dependencies(
    db: Session
) -> FindReportConfigUseCase:
    report_config_repository = ReportConfigRepository(db)
    return FindReportConfigUseCase(report_config_repository)

def set_delete_report_config_dependencies(
    db: Session
) -> DeleteReportConfigUseCase:
    report_config_repository = ReportConfigRepository(db)
    return DeleteReportConfigUseCase(report_config_repository)

def set_update_report_config_dependencies(
    db: Session
) -> UpdateReportConfigUseCase:
    report_config_repository = ReportConfigRepository(db)
    return UpdateReportConfigUseCase(report_config_repository)

def set_delete_metrics_dependencies(
    db: Session
) -> DeleteMetricsUseCase:
    users_repository = UsersRepository(db)
    commit_metrics_repository = RawCommitMetricsRepository(db)
    copilot_code_metrics_repository = RawCopilotCodeMetricsRepository(db)
    copilot_chat_metrics_repository = RawCopilotChatMetricsRepository(db)
    return DeleteMetricsUseCase(users_repository, commit_metrics_repository, copilot_code_metrics_repository, copilot_chat_metrics_repository)