from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from src.domain.entities.api_key import ApiKey
from src.infrastructure.database.api_keys.postgre.dtos.model import ApiKeyDbSchema
from src.infrastructure.database.api_keys.postgre.mappers.database_api_keys import DatabaseApiKeysMapper


class ApiKeysRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, api_key: ApiKey) -> None:
        record_to_save = DatabaseApiKeysMapper.to_database(api_key)
        self.db.add(record_to_save)
        self.db.commit()

    def find_by_prefix(self, key_prefix: str) -> List[ApiKey]:
        """Find all API keys matching a prefix (for hash validation)"""
        query = self.db.query(ApiKeyDbSchema)
        records = query.filter(ApiKeyDbSchema.key_prefix == key_prefix).all()
        return [DatabaseApiKeysMapper.to_domain(record) for record in records]

    def find_by_user_id(self, user_id: str) -> List[ApiKey]:
        """List all API keys for a user"""
        query = self.db.query(ApiKeyDbSchema)
        records = query.filter(ApiKeyDbSchema.user_id == user_id).all()
        return [DatabaseApiKeysMapper.to_domain(record) for record in records]

    def find_by_id(self, key_id: str) -> ApiKey | None:
        """Find a specific API key by ID"""
        query = self.db.query(ApiKeyDbSchema)
        record = query.filter(ApiKeyDbSchema.id == key_id).first()
        if not record:
            return None
        return DatabaseApiKeysMapper.to_domain(record)

    def delete(self, key_id: str) -> None:
        """Delete an API key"""
        query = self.db.query(ApiKeyDbSchema)
        query.filter(ApiKeyDbSchema.id == key_id).delete()
        self.db.commit()

    def update_last_used(self, key_id: str, timestamp: datetime) -> None:
        """Update the last_used_at timestamp"""
        query = self.db.query(ApiKeyDbSchema)
        query.filter(ApiKeyDbSchema.id == key_id).update({"last_used_at": timestamp})
        self.db.commit()
