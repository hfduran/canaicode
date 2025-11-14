from src.domain.entities.github_app import GitHubApp
from src.infrastructure.database.github_apps.postgre.github_apps_repository import GitHubAppsRepository


class FindGitHubAppUseCase:
  def __init__(
        self,
        github_apps_repository: GitHubAppsRepository,
    ) -> None:
        self.github_apps_repository = github_apps_repository

  def execute(self, user_id: str) -> GitHubApp | None:
      return self.github_apps_repository.find_by_user_id(user_id)