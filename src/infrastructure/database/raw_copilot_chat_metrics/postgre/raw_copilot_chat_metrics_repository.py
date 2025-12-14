from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.copilot_chat_metrics import CopilotChatMetrics
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.dtos.model import RawCopilotChatMetrics
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.mappers.database_raw_copilot_chat_metrics import DatabaseRawCopilotChatMetricsMapper

class RawCopilotChatMetricsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, copilot_chat_metrics: CopilotChatMetrics) -> None:
        record_to_save = DatabaseRawCopilotChatMetricsMapper.to_database(
            copilot_chat_metrics
        )

        self.db.add(record_to_save)
        self.db.commit()

    def upsert_many(self, copilot_chat_metrics_list: List[CopilotChatMetrics]) -> None:
        """
        Bulk upsert copilot chat metrics.
        Uses unique constraint on (team_name, date, ide, copilot_model) to detect duplicates.
        On conflict, updates metric values and metadata while preserving id and created_at.
        """
        if not copilot_chat_metrics_list:
            return

        try:
            # Convert domain entities to database models
            records_to_save = [
                DatabaseRawCopilotChatMetricsMapper.to_database(metrics)
                for metrics in copilot_chat_metrics_list
            ]

            # Build insert statement
            stmt = insert(RawCopilotChatMetrics).values([
                {
                    'id': record.id,
                    'team_name': record.team_name,
                    'date': record.date,
                    'ide': record.ide,
                    'copilot_model': record.copilot_model,
                    'total_users': record.total_users,
                    'total_chats': record.total_chats,
                    'copy_events': record.copy_events,
                    'insertion_events': record.insertion_events,
                    'created_at': record.created_at,
                    'user_id': record.user_id
                }
                for record in records_to_save
            ])

            # Handle conflicts on unique constraint (team_name, date, ide, copilot_model)
            # Update metric values and metadata, preserve id and created_at
            stmt = stmt.on_conflict_do_update(
                index_elements=['team_name', 'date', 'ide', 'copilot_model'],
                set_={
                    'total_users': stmt.excluded.total_users,
                    'total_chats': stmt.excluded.total_chats,
                    'copy_events': stmt.excluded.copy_events,
                    'insertion_events': stmt.excluded.insertion_events,
                    'user_id': stmt.excluded.user_id
                }
            )

            # Execute and commit once
            self.db.execute(stmt)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(
                f"Failed to bulk upsert {len(copilot_chat_metrics_list)} chat metrics: {str(e)}"
            ) from e

    def listByUserId(
        self,
        user_id: str,
        initial_date: Optional[datetime] = None,
        final_date: Optional[datetime] = None,
    ) -> List[CopilotChatMetrics]:
        query = self.db.query(RawCopilotChatMetrics)

        if initial_date:
            query = query.filter(RawCopilotChatMetrics.date >= initial_date)

        if final_date:
            query = query.filter(RawCopilotChatMetrics.date <= final_date)

        records = query.filter(RawCopilotChatMetrics.user_id == user_id).all()

        copilot_chat_metrics = map(
            lambda record: DatabaseRawCopilotChatMetricsMapper.to_domain(record),
            records,
        )

        return list(copilot_chat_metrics)
    
    def deleteByUserId(
        self, 
        user_id: str
    ) -> None:
        query = self.db.query(RawCopilotChatMetrics)
        query.filter(RawCopilotChatMetrics.user_id == user_id).delete()
        self.db.commit()
