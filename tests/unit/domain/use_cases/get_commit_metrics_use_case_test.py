from datetime import datetime, timezone
from typing import List
from unittest import TestCase
from unittest.mock import Mock

from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.value_objects.author import Author
from src.domain.entities.value_objects.repository import Repository
from src.domain.use_cases.get_commit_metrics_use_case import GetCommitMetricsUseCase


class TestGetCommitMetricsUseCase(TestCase):
    def test_get_commit_metrics_use_case(self) -> None:
        commit_metrics_repository = Mock()
        git_repo_consumer = Mock()
        date = datetime.strptime(
            "2025-11-05T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        ).replace(tzinfo=timezone.utc)
        commit_metrics = CommitMetrics(
            id="123",
            added_lines=9,
            author=Author(name="John Due", teams=["canaicode"]),
            date=date,
            hash="456123",
            language="python",
            removed_lines=2,
            repository=Repository(name="canaicode", team="canaicode"),
            created_at=date,
        )

        commit_metrics_list: List[CommitMetrics] = [commit_metrics, commit_metrics]

        git_repo_consumer.get_commits_by_date.return_value = commit_metrics_list

        get_commit_metrics_use_case = GetCommitMetricsUseCase(
            commit_metrics_repository, git_repo_consumer
        )

        get_commit_metrics_use_case.execute(date)

        self.assertEqual(commit_metrics_repository.put_item.call_count, 2)
        commit_metrics_repository.put_item.assert_called_with(commit_metrics)
