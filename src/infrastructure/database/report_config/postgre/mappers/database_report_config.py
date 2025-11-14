from typing import cast

from src.domain.entities.report_config import ReportConfig
from src.domain.entities.value_objects.enums.period import Period
from src.infrastructure.database.report_config.postgre.dtos.model import ReportConfigDbSchema


class DatabaseReportConfigMapper:
    @staticmethod
    def to_database(report_config: ReportConfig) -> ReportConfigDbSchema:
        return ReportConfigDbSchema(
            id=report_config.id,
            emails= ",".join(report_config.emails),
            period= report_config.period,
            user_id= report_config.user_id,
            created_at= report_config.created_at,
        )
    
    @staticmethod
    def to_domain(db_schema: ReportConfigDbSchema) -> ReportConfig:
        return ReportConfig(
            id=cast(str, db_schema.id),
            emails=cast(str, db_schema.emails).split(","),
            period=cast(Period, db_schema.period),
            user_id=cast(str, db_schema.user_id),
        )