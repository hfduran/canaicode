from datetime import datetime

from src.consumers.git_repo_consumer import GitRepoConsumer
from src.infrastructure.database.dynamo.raw_commit_metrics_repository import (
    RawCommitMetricsRepository,
)


class GetCommitMetricsUseCase:
    def __init__(
        self,
        commit_metrics_repository: RawCommitMetricsRepository,
        git_repo_consumer: GitRepoConsumer,
    ) -> None:
        self.commit_metrics_repository = commit_metrics_repository
        self.git_repo_consumer = git_repo_consumer

    def execute(self, date: datetime) -> None:
        commits_metrics = self.git_repo_consumer.get_commits_by_date(date)

        for commit_metrics in commits_metrics:
            self.commit_metrics_repository.put_item(commit_metrics)
