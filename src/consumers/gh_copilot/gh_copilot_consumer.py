import json
from typing import List
from config.config import CONFIG
from consumers.gh_copilot.gh_copilot_models import CopilotMetricsEntry


class GhCopilotConsumer:
    def getMetrics(self) -> None:
        with open(CONFIG.gh_copilot_metrics_file_path, "r") as file:
            data = json.load(file)

        result: List[CopilotMetricsEntry] = []
        for entry in data:
            model = CopilotMetricsEntry.model_validate(entry)
            result.append(model)

        for entry in result:
            print(
                entry.date,
                entry.total_active_users,
            )
