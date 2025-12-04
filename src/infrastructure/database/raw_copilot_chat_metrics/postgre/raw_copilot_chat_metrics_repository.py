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
        Skips duplicate records based on primary key (id).
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

            # Handle conflicts on primary key (id) - skip duplicates
            stmt = stmt.on_conflict_do_nothing(index_elements=['id'])

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
