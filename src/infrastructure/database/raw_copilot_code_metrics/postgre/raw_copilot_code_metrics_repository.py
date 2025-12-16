from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.copilot_code_metrics import CopilotCodeMetrics
from src.infrastructure.database.raw_copilot_code_metrics.postgre.dtos.model import RawCopilotCodeMetrics
from src.infrastructure.database.raw_copilot_code_metrics.postgre.mappers.database_raw_copilot_code_metrics import DatabaseRawCopilotCodeMetricsMapper

class RawCopilotCodeMetricsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, copilot_code_metrics: CopilotCodeMetrics) -> None:
        record_to_save = DatabaseRawCopilotCodeMetricsMapper.to_database(
            copilot_code_metrics
        )

        self.db.add(record_to_save)
        self.db.commit()

    def upsert_many(self, copilot_code_metrics_list: List[CopilotCodeMetrics]) -> None:
        """
        Bulk upsert copilot code metrics.
        Uses unique constraint on (date, ide, copilot_model, language) to detect duplicates.
        On conflict, updates metric values and metadata while preserving id and created_at.
        """
        if not copilot_code_metrics_list:
            return

        try:
            # Convert domain entities to database models
            records_to_save = [
                DatabaseRawCopilotCodeMetricsMapper.to_database(metrics)
                for metrics in copilot_code_metrics_list
            ]

            # Build insert statement with conflict resolution
            stmt = insert(RawCopilotCodeMetrics).values([
                {
                    'id': record.id,
                    'team_name': record.team_name,
                    'date': record.date,
                    'ide': record.ide,
                    'copilot_model': record.copilot_model,
                    'language': record.language,
                    'total_users': record.total_users,
                    'code_acceptances': record.code_acceptances,
                    'code_suggestions': record.code_suggestions,
                    'lines_accepted': record.lines_accepted,
                    'lines_suggested': record.lines_suggested,
                    'created_at': record.created_at,
                    'user_id': record.user_id
                }
                for record in records_to_save
            ])

            # Handle conflicts on unique constraint (date, ide, copilot_model, language)
            # Update metric values and metadata, preserve id and created_at
            stmt = stmt.on_conflict_do_update(
                index_elements=['user_id', 'date', 'ide', 'copilot_model', 'language'],
                set_={
                    'team_name': stmt.excluded.team_name,
                    'total_users': stmt.excluded.total_users,
                    'code_acceptances': stmt.excluded.code_acceptances,
                    'code_suggestions': stmt.excluded.code_suggestions,
                    'lines_accepted': stmt.excluded.lines_accepted,
                    'lines_suggested': stmt.excluded.lines_suggested
                }
            )

            # Execute and commit once
            self.db.execute(stmt)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(
                f"Failed to bulk upsert {len(copilot_code_metrics_list)} code metrics: {str(e)}"
            ) from e

    def listByUserId(
        self,
        user_id: str,
        initial_date: Optional[datetime] = None,
        final_date: Optional[datetime] = None,
        languages: Optional[List[str]] = None,
    ) -> List[CopilotCodeMetrics]:
        query = self.db.query(RawCopilotCodeMetrics)

        if initial_date:
            query = query.filter(RawCopilotCodeMetrics.date >= initial_date)

        if final_date:
            query = query.filter(RawCopilotCodeMetrics.date <= final_date)

        if languages:
            query = query.filter(RawCopilotCodeMetrics.language.in_(languages))

        records = query.filter(RawCopilotCodeMetrics.user_id == user_id).all()

        copilot_code_metrics = map(
            lambda record: DatabaseRawCopilotCodeMetricsMapper.to_domain(record),
            records,
        )

        return list(copilot_code_metrics)
    
    def deleteByUserId(
        self, 
        user_id: str
    ) -> None:
        query = self.db.query(RawCopilotCodeMetrics)
        query.filter(RawCopilotCodeMetrics.user_id == user_id).delete()
        self.db.commit()
