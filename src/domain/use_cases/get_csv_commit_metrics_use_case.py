from io import BytesIO
from typing import List

from src.consumers.git_metrics_xlsx.git_metrics_xlsx_consumer import GitCommitMetricsXlsxConsumer
from src.domain.entities.commit_metrics import CommitMetrics
from src.infrastructure.database.raw_commit_metrics.postgre.raw_commit_metrics_repository import RawCommitMetricsRepository


class GetXlsxCommitMetricsUseCase:
    def __init__(
        self,
        commit_metrics_repository: RawCommitMetricsRepository,
        git_commit_metrics_xlsx_consumer: GitCommitMetricsXlsxConsumer,
    ) -> None:
        self.commit_metrics_repository = commit_metrics_repository
        self.git_commit_metrics_xlsx_consumer = git_commit_metrics_xlsx_consumer

    def execute(self, file_content: BytesIO, user_id: str) -> List[CommitMetrics]:
        commits_metrics = self.git_commit_metrics_xlsx_consumer.execute(file_content, user_id)

        self.commit_metrics_repository.create_many(commits_metrics)

        return commits_metrics
