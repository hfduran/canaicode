from datetime import datetime
from src.consumers.gh_copilot.gh_copilot_models import CopilotMetricsEntry
from src.services.gh_copilot_services import GhCopilotServices, LocMetrics

from pytest import MonkeyPatch


class FakeGhCopilotConsumer:
    def __init__(self) -> None:
        pass

    def get_metrics(self) -> list[CopilotMetricsEntry]:
        with open("tests/data/gh_copilot_metrics_example.json", "r") as f:
            import json

            data = json.load(f)
            return [CopilotMetricsEntry.model_validate(entry) for entry in data]


def test_gh_copilot_services(monkeypatch: MonkeyPatch) -> None:
    start_date = datetime(2025, 1, 1).date()
    end_date = datetime(2025, 1, 3).date()

    expected_response: dict[str, LocMetrics] = {
        "python": LocMetrics(
            total_code_acceptances=140 + 70,
            total_code_suggestions=260 + 98,
            total_code_lines_accepted=300 + 300,
            total_code_lines_suggested=761 + 600,
        ),
    }

    monkeypatch.setattr(
        "src.services.gh_copilot_services.GhCopilotConsumer", FakeGhCopilotConsumer
    )

    response: dict[str, LocMetrics] = GhCopilotServices.summarize_metrics(
        start_date=start_date,
        end_date=end_date,
    )

    assert response == expected_response, (
        f"Expected {expected_response} but got {response}"
    )
