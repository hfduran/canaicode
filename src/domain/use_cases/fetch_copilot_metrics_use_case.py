import time
import requests
from typing import Any, Dict
from jose import jwt
from cryptography.fernet import Fernet
from src.domain.use_cases.get_copilot_metrics_use_case import GetCopilotMetricsUseCase
from src.infrastructure.database.github_apps.postgre.github_apps_repository import GitHubAppsRepository

class FetchCopilotMetricsUseCase:
    def __init__(
        self,
        github_apps_repository: GitHubAppsRepository,
        get_copilot_metrics_use_case: GetCopilotMetricsUseCase,
        encryption_key: str,
    ) -> None:
        self.github_apps_repository = github_apps_repository
        self.get_copilot_metrics_use_case = get_copilot_metrics_use_case
        self.fernet = Fernet(encryption_key.encode())

    def execute(self) -> None:
        github_apps = self.github_apps_repository.list()

        for github_app in github_apps:
            try:
                print(f"Starting fetching copilot metrics for github app: {github_app.id}")
                private_key = self.fernet.decrypt(github_app.private_key_encrypted.encode()).decode()
                metrics = self._fetch_metrics_from_github(
                    github_app.app_id,
                    github_app.installation_id,
                    github_app.organization_name,
                    private_key
                )
                print(f"metrics: {metrics}")
                self.get_copilot_metrics_use_case.execute(metrics, github_app.user_id)
            except Exception as e:
                print(f"Error during daily metrics collection: {e}")

    def _fetch_metrics_from_github(
        self,
        app_id: str,
        installation_id: str,
        organization_name: str,
        private_key: str
    ) -> Any:
        now = int(time.time())
        payload: Dict[str, str | int] = {
            "iat": now,
            "exp": now + (10 * 60),  # JWT valid for 10 minutes
            "iss": app_id,
        }
        jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
        }
        token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
        token_response = requests.post(token_url, headers=headers)
        token_response.raise_for_status()
        access_token = token_response.json()["token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        }
        metrics_url = f"https://api.github.com/orgs/{organization_name}/copilot/usage"
        metrics_response = requests.get(metrics_url, headers=headers)
        metrics_response.raise_for_status()

        return metrics_response.json()
