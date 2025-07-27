from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.domain.entities.value_objects.enums.period import Period


class CodeLineMetricsData(BaseModel):
    initial_date: datetime
    final_date: datetime
    net_changed_lines: int
    net_changed_lines_by_copilot: int
    percentage_changed_lines_by_copilot: float
    number_of_authors: int


class CommitMetricsData(BaseModel):
    initial_date: datetime
    final_date: datetime
    total_commits: int
    percentage_copilot_suggestions_accepted: float
    number_of_authors: int


class CalculatedMetrics(BaseModel):
    team: str
    languages: List[str]
    period: Period
    data: List[CodeLineMetricsData | CommitMetricsData]

class CopilotMetricsByLanguage(BaseModel):
    language: str
    code_acceptances: int
    code_suggestions: int
    lines_accepted: int
    lines_suggested: int
    percentage_code_acceptances: float
    percentage_lines_accepted: float
