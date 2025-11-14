from typing import cast
from src.domain.entities.github_app import GitHubApp
from src.infrastructure.database.github_apps.postgre.dtos.model import GitHubAppDbSchema


class DatabaseGitHubAppsMapper:
    @staticmethod
    def to_database(github_app: GitHubApp) -> GitHubAppDbSchema:
        return GitHubAppDbSchema(
            id=github_app.id,
            organization_name= github_app.organization_name,
            app_id= github_app.app_id,
            installation_id= github_app.installation_id,
            private_key_encrypted= github_app.private_key_encrypted,
            user_id= github_app.user_id,
            created_at= github_app.created_at,
        )
    
    @staticmethod
    def to_domain(db_schema: GitHubAppDbSchema) -> GitHubApp:
        return GitHubApp(
            id=cast(str, db_schema.id),
            organization_name=cast(str, db_schema.organization_name),
            app_id=cast(str, db_schema.app_id),
            installation_id=cast(str, db_schema.installation_id),
            private_key_encrypted=cast(str, db_schema.private_key_encrypted),
            user_id=cast(str, db_schema.user_id),
        )