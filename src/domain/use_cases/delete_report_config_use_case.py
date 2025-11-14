from fastapi import HTTPException
from src.infrastructure.database.report_config.postgre.report_config_repository import ReportConfigRepository


class DeleteReportConfigUseCase:
    def __init__(self, report_config_repository: ReportConfigRepository) -> None:
        self.report_config_repository = report_config_repository

    def execute(self, user_id: str, report_config_id: str) -> None:
        report_config = self.report_config_repository.find_by_id(report_config_id)

        if not report_config:
            raise HTTPException(status_code=404, detail="Report config not found")

        if report_config.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Cannot delete another user's report config"
            )

        self.report_config_repository.delete(report_config_id)