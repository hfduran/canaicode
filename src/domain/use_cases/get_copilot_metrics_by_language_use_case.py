from typing import DefaultDict, Dict, List
from src.domain.use_cases.dtos.calculated_metrics import CopilotMetricsByLanguage
from src.infrastructure.database.raw_copilot_code_metrics.postgre.raw_copilot_code_metrics_repository import RawCopilotCodeMetricsRepository


class GetCopilotMetricsByLanguageUseCase:
  def __init__(
        self,
        copilot_code_metrics_repository: RawCopilotCodeMetricsRepository,
    ) -> None:
        self.copilot_code_metrics_repository = copilot_code_metrics_repository

  def execute(self) -> List[CopilotMetricsByLanguage]:
    raw_copilot_code_metrics = self.copilot_code_metrics_repository.list()

    if (not raw_copilot_code_metrics):
      return []
    
    grouped_metrics: DefaultDict[str, Dict[str, int]] = DefaultDict(lambda: {
      "code_acceptances": 0,
      "code_suggestions": 0,
      "lines_accepted": 0,
      "lines_suggested": 0,
    })

    for metric in raw_copilot_code_metrics:
      language = metric.language
      grouped_metrics[language]["code_acceptances"] += metric.code_acceptances
      grouped_metrics[language]["code_suggestions"] += metric.code_suggestions
      grouped_metrics[language]["lines_accepted"] += metric.lines_accepted
      grouped_metrics[language]["lines_suggested"] += metric.lines_suggested

    response: List[CopilotMetricsByLanguage] = []
    for lang, values in grouped_metrics.items():
        code_suggestions = values["code_suggestions"]
        lines_suggested = values["lines_suggested"]
        code_acceptances = values["code_acceptances"]
        lines_accepted = values["lines_accepted"]

        percentage_code_acceptances = (
            code_acceptances / code_suggestions * 100
            if code_suggestions > 0 else 0.0
        )
            
        percentage_lines_accepted = (
            lines_accepted / lines_suggested * 100
            if lines_suggested > 0 else 0.0
        )

        response.append(CopilotMetricsByLanguage(
            language=lang,
            code_acceptances=code_acceptances,
            code_suggestions=code_suggestions,
            lines_accepted=lines_accepted,
            lines_suggested=lines_suggested,
            percentage_code_acceptances=percentage_code_acceptances,
            percentage_lines_accepted=percentage_lines_accepted
        ))

    return response