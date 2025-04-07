from datetime import date
from consumers.gh_copilot.gh_copilot_consumer import (
    CopilotMetricsEntry,
    GhCopilotConsumer,
)
from pydantic import BaseModel
from typer import echo


class LocMetrics(BaseModel):
    total_code_acceptances: int = 0
    total_code_suggestions: int = 0
    total_code_lines_accepted: int = 0
    total_code_lines_suggested: int = 0


class GhCopilotServices:
    @staticmethod
    def summarize_metrics(start_date: date, end_date: date) -> None:
        consumer = GhCopilotConsumer()
        result: list[CopilotMetricsEntry] = consumer.getMetrics()

        language_loc_metrics: dict[str, LocMetrics] = {}

        for entry in result:
            if entry.date is None:
                continue
            if entry.date < start_date or entry.date > end_date:
                continue

            completions_data = entry.copilot_ide_code_completions
            if completions_data is None:
                continue
            editors_data = completions_data.editors or []
            for editor_data in editors_data:
                models_data = editor_data.models or []
                for model_data in models_data:
                    languages_data = model_data.languages or []
                    for language_data in languages_data:
                        lang_name = language_data.name
                        if lang_name is None:
                            continue
                        language_loc_metrics.setdefault(lang_name, LocMetrics())
                        loc_metrics = language_loc_metrics[lang_name]
                        loc_metrics.total_code_acceptances += (
                            language_data.total_code_acceptances or 0
                        )
                        loc_metrics.total_code_suggestions += (
                            language_data.total_code_suggestions or 0
                        )
                        loc_metrics.total_code_lines_accepted += (
                            language_data.total_code_lines_accepted or 0
                        )
                        loc_metrics.total_code_lines_suggested += (
                            language_data.total_code_lines_suggested or 0
                        )

        for lang, loc_metrics in language_loc_metrics.items():
            echo()
            echo(f"Language: {lang}")
            echo(f"  Total Code Acceptances: {loc_metrics.total_code_acceptances}")
            echo(f"  Total Code Suggestions: {loc_metrics.total_code_suggestions}")
            echo(
                f"  Total Code Lines Accepted: {loc_metrics.total_code_lines_accepted}"
            )
            echo(
                f"  Total Code Lines Suggested: {loc_metrics.total_code_lines_suggested}"
            )
            echo("---")
        echo()
