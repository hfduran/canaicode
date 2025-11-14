from sqlalchemy.orm import Session
from typing import List

from src.domain.entities.report_config import ReportConfig
from src.infrastructure.database.report_config.postgre.dtos.model import ReportConfigDbSchema
from src.infrastructure.database.report_config.postgre.mappers.database_report_config import DatabaseReportConfigMapper


class ReportConfigRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, report_config: ReportConfig) -> None:
        record_to_save = DatabaseReportConfigMapper.to_database(
            report_config
        )

        self.db.add(record_to_save)
        self.db.commit()

    def find_by_id(
        self,
        report_config_id: str
    ) -> ReportConfig | None:
        query = self.db.query(ReportConfigDbSchema)

        record = query.filter(ReportConfigDbSchema.id == report_config_id).first()

        if(not record):
            return None

        return DatabaseReportConfigMapper.to_domain(record)

    def find_by_user_id(
        self,
        user_id: str
    ) -> ReportConfig | None:
        query = self.db.query(ReportConfigDbSchema)

        record = query.filter(ReportConfigDbSchema.user_id == user_id).first()

        if(not record):
            return None

        return DatabaseReportConfigMapper.to_domain(record)


    def list(
        self,
    ) -> List[ReportConfig]:
        query = self.db.query(ReportConfigDbSchema)

        records = query.all()

        report_configs = map(
            lambda record: DatabaseReportConfigMapper.to_domain(record), records
        )

        return list(report_configs)
    
    def delete(
        self, 
        report_config_id: str
    ) -> None:
        query = self.db.query(ReportConfigDbSchema)
        query.filter(ReportConfigDbSchema.id == report_config_id).delete()
        self.db.commit()