from fastapi import HTTPException

from src.infrastructure.database.github_apps.postgre.github_apps_repository import GitHubAppsRepository


class DeleteGitHubAppUseCase:
    def __init__(self, github_app_repository: GitHubAppsRepository) -> None:
        self.github_app_repository = github_app_repository

    def execute(self, user_id: str, github_app_id: str) -> None:
        github_app = self.github_app_repository.find_by_id(github_app_id)

        if not github_app:
            raise HTTPException(status_code=404, detail="Github App not found")

        if github_app.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Cannot delete another user's Github App"
            )

        self.github_app_repository.delete(github_app_id)