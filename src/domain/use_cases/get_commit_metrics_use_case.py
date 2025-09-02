from datetime import date
from typing import List

from src.consumers.git_repo_consumer import GitRepoConsumer
from src.domain.entities.commit_metrics import CommitMetrics
from src.infrastructure.database.raw_commit_metrics.postgre.raw_commit_metrics_repository import RawCommitMetricsRepository


class GetCommitMetricsUseCase:
    def __init__(
        self,
        commit_metrics_repository: RawCommitMetricsRepository,
        git_repo_consumer: GitRepoConsumer,
    ) -> None:
        self.commit_metrics_repository = commit_metrics_repository
        self.git_repo_consumer = git_repo_consumer

    def execute(self, date: date, team_name: str, user_id: str) -> List[CommitMetrics]:
        commits_metrics = self.git_repo_consumer.get_commits_by_date(date, team_name, user_id)

        for commit_metrics in commits_metrics:
            self.commit_metrics_repository.create(commit_metrics)

        return commits_metrics
