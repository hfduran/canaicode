from datetime import datetime
from typing import List, Optional

import pandas as pd  # type: ignore

from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.domain.entities.value_objects.enums.period import Period
from src.domain.entities.value_objects.enums.productivity_metric import (
    Productivity_metric,
)
from src.domain.use_cases.dtos.code_line_metrics import (
    CodeLineMetrics,
    CodeLineMetricsData,
)
from src.domain.use_cases.metrics_calculator import MetricsCalculator
from src.infrastructure.database.postgre.raw_commit_metrics.raw_commit_metrics_repository import (
    RawCommitMetricsRepository,
)
from src.infrastructure.database.postgre.raw_copilot_code_metrics.raw_copilot_code_metrics_repository import (
    RawCopilotCodeMetricsRepository,
)


class GetCalculatedMetricsUseCase:
    def __init__(
        self,
        commit_metrics_repository: RawCommitMetricsRepository,
        copilot_code_metrics_repository: RawCopilotCodeMetricsRepository,
    ) -> None:
        self.commit_metrics_repository = commit_metrics_repository
        self.copilot_code_metrics_repository = copilot_code_metrics_repository

    def execute(
        self,
        team: str,
        period: Period,
        productivity_metric: Productivity_metric,
        initial_date: Optional[datetime],
        final_date: Optional[datetime],
        languages: Optional[List[str]],
    ) -> CodeLineMetrics | None:
        raw_commit_metrics = self.commit_metrics_repository.listByTeam(
            team, initial_date, final_date, languages
        )

        if not raw_commit_metrics:
            return None

        raw_copilot_code_metrics = self.copilot_code_metrics_repository.listByTeam(
            team, initial_date, final_date, languages
        )

        productivity_metric_map = {
            Productivity_metric.code_lines: self.get_code_lines_metrics,
            Productivity_metric.commits: self.get_commit_metrics,
        }

        result = productivity_metric_map[productivity_metric](
            raw_commit_metrics, raw_copilot_code_metrics, period
        )

        return result

    def get_code_lines_metrics(
        self,
        raw_commit_metrics: List[CommitMetrics],
        raw_copilot_code_metrics: List[CopilotCodeMetrics],
        period: Period,
    ) -> CodeLineMetrics | None:
        df_commit_metrics = pd.DataFrame(
            [{"metrics": c, "date": c.date} for c in raw_commit_metrics]
        )
        df_copilot_code_metrics = pd.DataFrame(
            [{"metrics": c, "date": c.date} for c in raw_copilot_code_metrics]
        )

        grouped_commit_metrics = df_commit_metrics.groupby(  # type: ignore
            pd.Grouper(key="date", freq=period)
        )

        grouped_copilot_code_metrics = df_copilot_code_metrics.groupby(  # type: ignore
            pd.Grouper(key="date", freq=period)
        )

        response = CodeLineMetrics(
            team=raw_commit_metrics[0].repository.team,
            languages=[],
            period=period,
            data=[],
        )

        total_added_lines: int = 0

        for period_final_date, commit_metrics_df in grouped_commit_metrics:  # type: ignore
            authors = []
            relative_added_lines = 0
            for commit_metrics in commit_metrics_df["metrics"]:  # type: ignore
                if commit_metrics.language not in response.languages:  # type: ignore
                    response.languages.append(commit_metrics.language)  # type: ignore
                if commit_metrics.author.name not in authors:  # type: ignore
                    authors.append(commit_metrics.author.name)  # type: ignore
                relative_added_lines += MetricsCalculator.calculate_gross_productivity(
                    [commit_metrics]
                )
                total_added_lines += commit_metrics.added_lines  # type: ignore

            response.data.append(
                CodeLineMetricsData(
                    initial_date=period_final_date.to_period(  # type: ignore
                        "M"
                    ).start_time.to_pydatetime(),
                    final_date=period_final_date.to_pydatetime(),  # type: ignore
                    relative_added_lines=relative_added_lines,
                    percentage_added_lines_by_copilot=0,
                    number_of_authors=authors.__len__(),
                )
            )

        for (
            copilot_period_final_date,  # type: ignore
            copilot_code_metrics_df,
        ) in grouped_copilot_code_metrics:
            index = next(
                i
                for i, data in enumerate(response.data)
                if data.final_date == copilot_period_final_date
            )
            total_added_lines_by_copilot = MetricsCalculator.calculate_gross_use_of_AI(
                copilot_code_metrics_df["metrics"].to_list()  # type: ignore
            )
            percentage_added_lines_by_copilot = (  # type: ignore
                total_added_lines_by_copilot / total_added_lines
            )
            response.data[
                index
            ].percentage_added_lines_by_copilot = percentage_added_lines_by_copilot

        return response

    def get_commit_metrics(
        self,
        raw_commit_metrics: List[CommitMetrics],
        raw_copilot_code_metrics: List[CopilotCodeMetrics],
        period: Period,
    ) -> CodeLineMetrics | None:
        return None
