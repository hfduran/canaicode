from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.infrastructure.database.dynamo.raw_copilot_chat_metrics_repository import (
    RawCopilotChatMetricsRepository,
)


class TestRawCopilotChatMetricsRepository(TestCase):
    @patch("boto3.resource")
    def test_raw_copilot_chat_metrics_repository_get_item(
        self, mock_boto_resource: MagicMock
    ) -> None:
        mock_table = MagicMock()
        mock_table.get_item.return_value = {
            "Item": {
                "id": "123",
                "team": "canaicode",
                "date": "2025-11-05T12:38:22.000Z",
                "IDE": "VSCode",
                "copilot_model": "default",
                "total_users": "9",
                "total_chats": "1",
                "copy_events": "1",
                "insertion_events": "1",
            }
        }

        mock_dynamodb = mock_boto_resource.return_value
        mock_dynamodb.Table.return_value = mock_table

        expected_response = CopilotChatMetrics(
            id="123",
            team="canaicode",
            date=datetime.strptime(
                "2025-11-05T12:38:22.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc),
            IDE="VSCode",
            copilot_model="default",
            total_users=9,
            total_chats=1,
            copy_events=1,
            insertion_events=1,
        )

        raw_copilot_chat_metrics_repository = RawCopilotChatMetricsRepository()

        item = raw_copilot_chat_metrics_repository.get_item("123")

        self.assertEqual(
            item,
            expected_response,
        )
        mock_table.get_item.assert_called_once_with(Key={"id": "123"})

    @patch("boto3.resource")
    def test_raw_copilot_chat_metrics_repository_get_item_no_item(
        self, mock_boto_resource: MagicMock
    ) -> None:
        mock_table = MagicMock()
        mock_table.get_item.return_value = {"Item": {}}

        mock_dynamodb = mock_boto_resource.return_value
        mock_dynamodb.Table.return_value = mock_table

        raw_copilot_chat_metrics_repository = RawCopilotChatMetricsRepository()

        item = raw_copilot_chat_metrics_repository.get_item("123")

        self.assertEqual(
            item,
            None,
        )
        mock_table.get_item.assert_called_once_with(Key={"id": "123"})

    @patch("boto3.resource")
    def test_raw_copilot_chat_metrics_repository_put_item(
        self, mock_boto_resource: MagicMock
    ) -> None:
        mock_table = MagicMock()
        mock_dynamodb = mock_boto_resource.return_value
        mock_dynamodb.Table.return_value = mock_table

        raw_copilot_chat_metrics_repository = RawCopilotChatMetricsRepository()

        copilot_chat_metrics = CopilotChatMetrics(
            id="123",
            team="canaicode",
            date=datetime.strptime(
                "2025-11-05T12:38:22.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc),
            IDE="VSCode",
            copilot_model="default",
            total_users=9,
            total_chats=1,
            copy_events=1,
            insertion_events=1,
        )

        raw_copilot_chat_metrics_repository.put_item(copilot_chat_metrics)

        mock_table.put_item.assert_called_once_with(
            Item=copilot_chat_metrics.model_dump()
        )
