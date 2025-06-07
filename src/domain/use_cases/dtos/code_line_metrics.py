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


class CodeLineMetrics(BaseModel):
    team: str
    languages: List[str]
    period: Period
    data: List[CodeLineMetricsData]
