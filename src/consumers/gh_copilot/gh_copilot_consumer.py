import json
import uuid
from datetime import datetime
from typing import Dict, List

from config.config import CONFIG
from consumers.gh_copilot.gh_copilot_models import CopilotMetricsEntry
from src.consumers.gh_copilot.gh_copilot_models_dto import CopilotMetricsEntryDTO
from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.domain.entities.copilot_metrics import CopilotMetrics
from src.domain.entities.value_objects.team import Team


class GhCopilotConsumer:
    def get_metrics(self) -> list[CopilotMetricsEntry]:
        with open(CONFIG.gh_copilot_metrics_file_path, "r") as file:
            data = json.load(file)

        result: list[CopilotMetricsEntry] = []
        for entry in data:
            model = CopilotMetricsEntry.model_validate(entry)
            result.append(model)

        return result

    def get_metrics_by_date(self, date: datetime) -> Dict[str, List[CopilotMetrics]]:
        with open(CONFIG.gh_copilot_metrics_file_path, "r") as file:
            data: List[CopilotMetricsEntryDTO] = json.load(file)

        result: Dict[str, List[CopilotMetrics]] = {"code": [], "chat": []}

        for entry in data:
            entry_date = datetime.strptime(entry.date, "%Y-%m-%d")
            if entry_date == date:
                for editor in entry.copilot_ide_code_completions.editors:
                    for model in editor.models:
                        for language in model.languages:
                            result["code"].append(
                                CopilotCodeMetrics(
                                    id=str(uuid.uuid4()),
                                    code_acceptances=language.total_code_acceptances,
                                    code_suggestions=language.total_code_suggestions,
                                    copilot_model=model.name,
                                    date=entry_date,
                                    IDE=editor.name,
                                    language=language.name,
                                    lines_accepted=language.total_code_lines_accepted,
                                    lines_suggested=language.total_code_lines_suggested,
                                    team=Team(name=""),  # TODO: team name
                                    total_users=language.total_engaged_users,
                                )
                            )

                for chat_editor in entry.copilot_ide_chat.editors:
                    for chat_model in chat_editor.models:
                        result["chat"].append(
                            CopilotChatMetrics(
                                id=str(uuid.uuid4()),
                                copilot_model=chat_model.name,
                                copy_events=chat_model.total_chat_copy_events,
                                date=entry_date,
                                IDE=chat_editor.name,
                                insertion_events=chat_model.total_chat_insertion_events,
                                team=Team(name=""),  # TODO: team name
                                total_chats=chat_model.total_chats,
                                total_users=chat_model.total_engaged_users,
                            )
                        )

        return result
