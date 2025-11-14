from src.domain.entities.report_config import ReportConfig
from src.infrastructure.database.report_config.postgre.report_config_repository import ReportConfigRepository


class FindReportConfigUseCase:
  def __init__(
        self,
        report_config_repository: ReportConfigRepository,
    ) -> None:
        self.report_config_repository = report_config_repository

  def execute(self, user_id: str) -> ReportConfig | None:
      return self.report_config_repository.find_by_user_id(user_id)