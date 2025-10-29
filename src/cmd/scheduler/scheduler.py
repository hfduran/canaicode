import os
from apscheduler.schedulers.blocking import BlockingScheduler
from repositories.github_apps_repository import GitHubAppsRepository
from use_cases.fetch_copilot_metrics_use_case import FetchCopilotMetricsUseCase

FERNET_KEY = os.getenv("FERNET_KEY")
scheduler = BlockingScheduler()

repository = GitHubAppsRepository()
use_case = FetchCopilotMetricsUseCase(
    github_apps_repository=repository,
    encryption_key=FERNET_KEY,
)

@scheduler.scheduled_job('interval', days=1)
def fetch_metrics_job():
    print("Starting GitHub Copilot metrics collection")
    try:
        use_case.execute()
        print("Metrics collection completed successfully")
    except Exception as e:
        print(f"Error during metrics collection: {e}")

if __name__ == "__main__":
    scheduler.start()
