import json
from config.config import CONFIG
from consumers.gh_copilot.gh_copilot_models import CopilotMetricsEntry


class GhCopilotConsumer:
    def get_metrics(self) -> list[CopilotMetricsEntry]:
        with open(CONFIG.gh_copilot_metrics_file_path, "r") as file:
            data = json.load(file)

        result: list[CopilotMetricsEntry] = []
        for entry in data:
            model = CopilotMetricsEntry.model_validate(entry)
            result.append(model)

        return result
