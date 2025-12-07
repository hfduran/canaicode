from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd  # type: ignore

from src.domain.entities.commit_metrics import CommitMetrics
from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.domain.entities.value_objects.enums.period import Period
from src.domain.entities.value_objects.enums.productivity_metric import (
    Productivity_metric,
)
from src.domain.use_cases.dtos.calculated_metrics import (
    CalculatedMetrics,
    CodeLineMetricsData,
    CommitMetricsData,
)
from src.domain.use_cases.metrics_calculator import MetricsCalculator
from src.infrastructure.database.raw_commit_metrics.postgre.raw_commit_metrics_repository import RawCommitMetricsRepository
from src.infrastructure.database.raw_copilot_code_metrics.postgre.raw_copilot_code_metrics_repository import RawCopilotCodeMetricsRepository


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
        user_id: str,
        period: Period,
        productivity_metric: Productivity_metric,
        initial_date: Optional[datetime] = None,
        final_date: Optional[datetime] = None,
        languages: Optional[List[str]] = None,
    ) -> CalculatedMetrics:
        raw_commit_metrics = self.commit_metrics_repository.listByUserId(
            user_id, initial_date, final_date, languages
        )

        if not raw_commit_metrics:
            return CalculatedMetrics(
                user_id=user_id,
                languages=[],
                period=period,
                data=[],
            )

        raw_copilot_code_metrics = self.copilot_code_metrics_repository.listByUserId(
            user_id, initial_date, final_date, languages
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
    ) -> CalculatedMetrics:
        df_commit_metrics = pd.DataFrame(
            [{"metrics": c, "date": c.date} for c in raw_commit_metrics]
        )
        df_copilot_code_metrics = pd.DataFrame(
            [{"metrics": c, "date": c.date} for c in raw_copilot_code_metrics],
            columns=["metrics", "date"]
        )
        df_copilot_code_metrics["date"] = pd.to_datetime(df_copilot_code_metrics["date"], errors="coerce") # type: ignore

        grouped_commit_metrics = df_commit_metrics.groupby(  # type: ignore
            pd.Grouper(key="date", freq=period)
        )

        grouped_copilot_code_metrics = df_copilot_code_metrics.groupby(  # type: ignore
            pd.Grouper(key="date", freq=period)
        )

        response = CalculatedMetrics(
            user_id=raw_commit_metrics[0].user_id,
            languages=[],
            period=period,
            data=[],
        )

        total_added_lines: int = 0

        for period_final_date, commit_metrics_df in grouped_commit_metrics:  # type: ignore
            authors = []
            net_changed_lines = 0
            for commit_metrics in commit_metrics_df["metrics"]:  # type: ignore
                if commit_metrics.language not in response.languages:  # type: ignore
                    response.languages.append(commit_metrics.language)  # type: ignore
                if commit_metrics.author.name not in authors:  # type: ignore
                    authors.append(commit_metrics.author.name)  # type: ignore
                net_changed_lines += MetricsCalculator.calculate_gross_productivity(
                    [commit_metrics]
                )
                total_added_lines += commit_metrics.added_lines  # type: ignore

            response.data.append(
                CodeLineMetricsData(
                    initial_date=period_final_date.to_period(  # type: ignore
                        period
                    ).start_time.to_pydatetime(),
                    final_date=period_final_date.to_pydatetime(),  # type: ignore
                    net_changed_lines=net_changed_lines,
                    net_changed_lines_by_copilot=0,
                    percentage_changed_lines_by_copilot=0,
                    number_of_authors=authors.__len__(),
                )
            )

        for (
            copilot_period_final_date,  # type: ignore
            copilot_code_metrics_df,
        ) in grouped_copilot_code_metrics:
            index = next(
                (i for i, data in enumerate(response.data)
                if data.final_date == copilot_period_final_date),
                None
            )
            if index is None:
                continue
            total_added_lines_by_copilot = MetricsCalculator.calculate_gross_use_of_AI_lines(
                copilot_code_metrics_df["metrics"].to_list()  # type: ignore
            )
            percentage_changed_lines_by_copilot = (  # type: ignore
                total_added_lines_by_copilot / total_added_lines
            )
            response.data[index].percentage_changed_lines_by_copilot = percentage_changed_lines_by_copilot # type: ignore
            response.data[index].net_changed_lines_by_copilot = round(percentage_changed_lines_by_copilot * response.data[index].net_changed_lines) # type: ignore

        return response

    def get_commit_metrics(
        self,
        raw_commit_metrics: List[CommitMetrics],
        period: Period,
    ) -> CalculatedMetrics:

        aggregated_by_hash: Dict[str, CommitMetrics] = {}

        languages: List[str] = []
        authors: List[str] = []

        for c in raw_commit_metrics:
            if c.language not in languages:
                languages.append(c.language)

            if c.author.name not in authors:
                authors.append(c.author.name)

            if c.hash not in aggregated_by_hash:
                aggregated_by_hash[c.hash] = CommitMetrics(
                    hash=c.hash,
                    user_id=c.user_id,
                    date=c.date,
                    language=c.language,
                    author=c.author,
                    added_lines=0,
                    removed_lines=0,
                )
            else:
                if c.date > aggregated_by_hash[c.hash].date:
                    aggregated_by_hash[c.hash].date = c.date

        aggregated_list = list(aggregated_by_hash.values())

        response = CalculatedMetrics(
            user_id=aggregated_list[0].user_id,
            languages=languages,
            period=period,
            data=[],
        )

        df_commit_metrics = pd.DataFrame(
            [{"metrics": c, "date": c.date} for c in aggregated_list]
        )

        grouped_commit_metrics = df_commit_metrics.groupby(
            pd.Grouper(key="date", freq=period)
        )

        for period_final_date, commit_metrics_df in grouped_commit_metrics:
            response.data.append(
                CommitMetricsData(
                    initial_date=period_final_date
                        .to_period(period)
                        .start_time
                        .to_pydatetime(),
                    final_date=period_final_date.to_pydatetime(),
                    total_commits=len(commit_metrics_df["metrics"]),
                    number_of_authors=len(authors),
                )
            )

        return response
