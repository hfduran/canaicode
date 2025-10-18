import uuid
from cryptography.fernet import Fernet
from src.domain.entities.github_app import GitHubApp
from src.infrastructure.database.github_apps.postgre.github_apps_repository import GitHubAppsRepository


class CreateGitHubAppUseCase:
  def __init__(
        self,
        github_apps_repository: GitHubAppsRepository,
        encryption_key: str,
    ) -> None:
        self.github_apps_repository = github_apps_repository
        self.fernet = Fernet(encryption_key.encode())

  def execute(self, user_id: str, organization_name: str, app_id: str, installation_id: str, private_key: str) -> None:
      encrypted_private_key = self.fernet.encrypt(private_key.encode()).decode()

      github_app = GitHubApp(
          id=str(uuid.uuid4()),
          app_id=app_id,
          installation_id=installation_id,
          organization_name=organization_name,
          private_key_encrypted=encrypted_private_key,
          user_id=user_id
      )

      self.github_apps_repository.create(github_app)