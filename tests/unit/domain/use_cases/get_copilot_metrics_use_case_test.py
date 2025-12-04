from datetime import datetime, timezone
from typing import Dict, List
from unittest import TestCase
from unittest.mock import Mock

from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.domain.entities.copilot_metrics import CopilotMetrics
from src.domain.entities.value_objects.team import Team
from src.domain.use_cases.get_copilot_metrics_use_case import GetCopilotMetricsUseCase


class TestGetCopilotMetricsUseCase(TestCase):
    def test_get_copilot_metrics_use_case(self) -> None:
        copilot_code_metrics_repository = Mock()
        copilot_chat_metrics_repository = Mock()
        github_copilot_consumer = Mock()
        date = datetime.strptime(
            "2025-11-05T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        ).replace(tzinfo=timezone.utc)
        copilot_code_metrics = CopilotCodeMetrics(
            id="123",
            user_id="test-user-id",
            team=Team(
                name="canaicode",
            ),
            date=date,
            IDE="VSCode",
            copilot_model="default",
            language="python",
            total_users=9,
            code_acceptances=1,
            code_suggestions=1,
            lines_accepted=1,
            lines_suggested=1,
            created_at=date,
        )
        copilot_chat_metrics = CopilotChatMetrics(
            id="123",
            user_id="test-user-id",
            team=Team(
                name="canaicode",
            ),
            date=date,
            IDE="VSCode",
            copilot_model="default",
            total_users=9,
            total_chats=1,
            copy_events=1,
            insertion_events=1,
            created_at=date,
        )

        copilot_metrics: Dict[str, List[CopilotMetrics]] = {
            "code": [copilot_code_metrics, copilot_code_metrics],
            "chat": [copilot_chat_metrics, copilot_chat_metrics],
        }

        github_copilot_consumer.get_metrics.return_value = copilot_metrics

        get_copilot_metrics_use_case = GetCopilotMetricsUseCase(
            copilot_code_metrics_repository,
            copilot_chat_metrics_repository,
            github_copilot_consumer,
        )

        # execute() now takes data (dict) and user_id
        test_data = {"test": "data"}
        get_copilot_metrics_use_case.execute(test_data, "test-user-id")

        # Verify upsert_many is called once with list of metrics
        self.assertEqual(copilot_code_metrics_repository.upsert_many.call_count, 1)
        copilot_code_metrics_repository.upsert_many.assert_called_with(
            [copilot_code_metrics, copilot_code_metrics]
        )
        self.assertEqual(copilot_chat_metrics_repository.upsert_many.call_count, 1)
        copilot_chat_metrics_repository.upsert_many.assert_called_with(
            [copilot_chat_metrics, copilot_chat_metrics]
        )
