from typing import List
from fastapi import HTTPException
from src.domain.entities.report_config import ReportConfig
from src.domain.entities.value_objects.enums.period import Period
from src.infrastructure.database.report_config.postgre.report_config_repository import ReportConfigRepository


class UpdateReportConfigUseCase:
    def __init__(self, report_config_repository: ReportConfigRepository) -> None:
        self.report_config_repository = report_config_repository

    def execute(self, user_id: str, report_config_id: str, emails: List[str], period: Period) -> ReportConfig:
        persisted_report_config = self.report_config_repository.find_by_id(report_config_id)

        if not persisted_report_config:
            raise HTTPException(status_code=404, detail="Report config not found")

        if persisted_report_config.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Cannot update another user's report config"
            )
        
        report_config = ReportConfig(
            id=persisted_report_config.id,
            emails=emails,
            period=period,
            user_id=user_id,
            created_at=persisted_report_config.created_at
        )

        self.report_config_repository.update(report_config)

        return report_config