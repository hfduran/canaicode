from datetime import datetime
from typing import List
import uuid

from src.domain.entities.report_config import ReportConfig
from src.domain.entities.value_objects.enums.period import Period
from src.infrastructure.database.report_config.postgre.report_config_repository import ReportConfigRepository


class CreateReportConfigUseCase:
  def __init__(
        self,
        report_config_repository: ReportConfigRepository,
    ) -> None:
        self.report_config_repository = report_config_repository

  def execute(self, user_id: str, emails: List[str], period: Period) -> ReportConfig:

      report_config = ReportConfig(
          id=str(uuid.uuid4()),
          emails=emails,
          period=period,
          user_id=user_id,
          created_at=datetime.now()
      )

      self.report_config_repository.create(report_config)

      return report_config