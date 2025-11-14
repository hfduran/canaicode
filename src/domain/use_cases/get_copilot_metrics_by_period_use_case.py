from datetime import datetime
import pandas as pd  # type: ignore
from typing import List, Optional
from src.domain.entities.value_objects.enums.period import Period
from src.domain.use_cases.dtos.calculated_metrics import CopilotMetricsByPeriod
from src.domain.use_cases.metrics_calculator import MetricsCalculator
from src.infrastructure.database.raw_copilot_code_metrics.postgre.raw_copilot_code_metrics_repository import RawCopilotCodeMetricsRepository


class GetCopilotMetricsByPeriodUseCase:
  def __init__(
        self,
        copilot_code_metrics_repository: RawCopilotCodeMetricsRepository,
    ) -> None:
        self.copilot_code_metrics_repository = copilot_code_metrics_repository

  def execute(self, user_id: str, period: Period, initial_date: Optional[datetime] = None, final_date: Optional[datetime] = None) -> List[CopilotMetricsByPeriod]:
      raw_copilot_code_metrics = self.copilot_code_metrics_repository.listByUserId(user_id, initial_date, final_date)

      if (not raw_copilot_code_metrics):
        return []
      
      df_copilot_code_metrics = pd.DataFrame(
            [{"metrics": c, "date": c.date} for c in raw_copilot_code_metrics],
            columns=["metrics", "date"]
        )
      
      grouped_copilot_code_metrics = df_copilot_code_metrics.groupby(  # type: ignore
            pd.Grouper(key="date", freq=period)
        )
      
      response: List[CopilotMetricsByPeriod] = []

      for (
            copilot_period_final_date,  # type: ignore
            copilot_code_metrics_df,
        ) in grouped_copilot_code_metrics:
            total_code_acceptances = MetricsCalculator.calculate_gross_use_of_AI(
                copilot_code_metrics_df["metrics"].to_list()  # type: ignore
            )

            percentage_code_acceptances = MetricsCalculator.calculate_relative_use_of_AI(
                copilot_code_metrics_df["metrics"].to_list()  # type: ignore
            )

            total_lines_accepted = MetricsCalculator.calculate_gross_use_of_AI_lines(
                copilot_code_metrics_df["metrics"].to_list()  # type: ignore
            )

            percentage_lines_accepted = MetricsCalculator.calculate_relative_use_of_AI_lines(
                copilot_code_metrics_df["metrics"].to_list()  # type: ignore
            )
            
            response.append(CopilotMetricsByPeriod(
                period_final_date=copilot_period_final_date.to_pydatetime(),  # type: ignore
                period_initial_date=copilot_period_final_date.to_period(  # type: ignore
                    period
                ).start_time.to_pydatetime(),
                total_code_acceptances=total_code_acceptances,
                percentage_code_acceptances=percentage_code_acceptances,
                total_lines_accepted=total_lines_accepted,
                percentage_lines_accepted=percentage_lines_accepted
            ))

      return response
