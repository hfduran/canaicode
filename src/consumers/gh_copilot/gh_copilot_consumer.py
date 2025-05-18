import json
import uuid
from datetime import date
from typing import Dict, List

from src.config.config import CONFIG
from src.consumers.gh_copilot.gh_copilot_models import CopilotMetricsEntry
from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
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

    def get_metrics_by_date(
        self, date: date
    ) -> Dict[str, List[CopilotCodeMetrics | CopilotChatMetrics]]:
        with open(CONFIG.gh_copilot_metrics_file_path, "r") as file:
            data = json.load(file)

        result: Dict[str, List[CopilotCodeMetrics | CopilotChatMetrics]] = {
            "code": [],
            "chat": [],
        }

        for entry in data:
            parsed_entry = CopilotMetricsEntry.model_validate(entry)
            if parsed_entry.date == date:
                for editor in parsed_entry.copilot_ide_code_completions.editors:  # type: ignore
                    for model in editor.models:  # type: ignore
                        for language in model.languages:  # type: ignore
                            result["code"].append(
                                CopilotCodeMetrics(
                                    id=str(uuid.uuid4()),
                                    code_acceptances=language.total_code_acceptances,  # type: ignore
                                    code_suggestions=language.total_code_suggestions,  # type: ignore
                                    copilot_model=model.name,  # type: ignore
                                    date=parsed_entry.date,  # type: ignore
                                    IDE=editor.name,  # type: ignore
                                    language=language.name,  # type: ignore
                                    lines_accepted=language.total_code_lines_accepted,  # type: ignore
                                    lines_suggested=language.total_code_lines_suggested,  # type: ignore
                                    team=Team(name=""),  # TODO: team name
                                    total_users=language.total_engaged_users,  # type: ignore
                                )
                            )

                for chat_editor in parsed_entry.copilot_ide_chat.editors:  # type: ignore
                    for chat_model in chat_editor.models:  # type: ignore
                        result["chat"].append(
                            CopilotChatMetrics(
                                id=str(uuid.uuid4()),
                                copilot_model=chat_model.name,  # type: ignore
                                copy_events=chat_model.total_chat_copy_events,  # type: ignore
                                date=parsed_entry.date,  # type: ignore
                                IDE=chat_editor.name,  # type: ignore
                                insertion_events=chat_model.total_chat_insertion_events,  # type: ignore
                                team=Team(name=""),  # TODO: team name
                                total_chats=chat_model.total_chats,  # type: ignore
                                total_users=chat_model.total_engaged_users,  # type: ignore
                            )
                        )

        return result
