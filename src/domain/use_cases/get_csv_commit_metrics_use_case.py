from typing import List, TextIO

from src.consumers.git_metrics_csv.git_metrics_csv_consumer import GitCommitMetricsCsvConsumer
from src.domain.entities.commit_metrics import CommitMetrics
from src.infrastructure.database.raw_commit_metrics.postgre.raw_commit_metrics_repository import RawCommitMetricsRepository


class GetCsvCommitMetricsUseCase:
    def __init__(
        self,
        commit_metrics_repository: RawCommitMetricsRepository,
        git_commit_metrics_csv_consumer: GitCommitMetricsCsvConsumer,
    ) -> None:
        self.commit_metrics_repository = commit_metrics_repository
        self.git_commit_metrics_csv_consumer = git_commit_metrics_csv_consumer

    def execute(self, file_content: TextIO) -> List[CommitMetrics]:
        commits_metrics = self.git_commit_metrics_csv_consumer.execute(file_content)

        for commit_metrics in commits_metrics:
            self.commit_metrics_repository.create(commit_metrics)

        return commits_metrics
