from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.value_objects.author import Author
from src.domain.entities.value_objects.repository import Repository
from src.infrastructure.database.dynamo.raw_commit_metrics_repository import (
    RawCommitMetricsRepository,
)


class TestRawCommitMetricsRepository(TestCase):
    @patch("boto3.resource")
    def test_raw_commit_metrics_repository_get_item(
        self, mock_boto_resource: MagicMock
    ) -> None:
        mock_table = MagicMock()
        mock_table.get_item.return_value = {
            "Item": {
                "id": "123",
                "hash": "123456",
                "repository": {"name": "canaicode", "team": "canaicode"},
                "date": "2025-11-05T12:38:22.000Z",
                "author": {"name": "johnDue", "teams": ["canaicode"]},
                "language": "python",
                "added_lines": "9",
                "removed_lines": "1",
            }
        }

        mock_dynamodb = mock_boto_resource.return_value
        mock_dynamodb.Table.return_value = mock_table

        expected_response = CommitMetrics(
            id="123",
            hash="123456",
            repository=Repository(name="canaicode", team="canaicode"),
            date=datetime.strptime(
                "2025-11-05T12:38:22.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc),
            author=Author(name="johnDue", teams=["canaicode"]),
            language="python",
            added_lines=9,
            removed_lines=1,
        )

        raw_commit_metrics_repository = RawCommitMetricsRepository()

        item = raw_commit_metrics_repository.get_item("123")

        self.assertEqual(
            item,
            expected_response,
        )
        mock_table.get_item.assert_called_once_with(Key={"id": "123"})

    @patch("boto3.resource")
    def test_raw_commit_metrics_repository_get_item_no_item(
        self, mock_boto_resource: MagicMock
    ) -> None:
        mock_table = MagicMock()
        mock_table.get_item.return_value = {"Item": {}}

        mock_dynamodb = mock_boto_resource.return_value
        mock_dynamodb.Table.return_value = mock_table

        raw_commit_metrics_repository = RawCommitMetricsRepository()

        item = raw_commit_metrics_repository.get_item("123")

        self.assertEqual(
            item,
            None,
        )
        mock_table.get_item.assert_called_once_with(Key={"id": "123"})

    @patch("boto3.resource")
    def test_raw_commit_metrics_repository_put_item(
        self, mock_boto_resource: MagicMock
    ) -> None:
        mock_table = MagicMock()
        mock_dynamodb = mock_boto_resource.return_value
        mock_dynamodb.Table.return_value = mock_table

        raw_commit_metrics_repository = RawCommitMetricsRepository()

        commit = CommitMetrics(
            id="123",
            hash="123456",
            repository=Repository(name="canaicode", team="canaicode"),
            date=datetime.strptime(
                "2025-11-05T12:38:22.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc),
            author=Author(name="johnDue", teams=["canaicode"]),
            language="python",
            added_lines=9,
            removed_lines=1,
        )

        raw_commit_metrics_repository.put_item(commit)

        mock_table.put_item.assert_called_once_with(Item=commit.model_dump())
