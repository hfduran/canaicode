from datetime import datetime
from typing import Optional, cast
from src.domain.entities.api_key import ApiKey
from src.infrastructure.database.api_keys.postgre.dtos.model import ApiKeyDbSchema


class DatabaseApiKeysMapper:
    @staticmethod
    def to_database(api_key: ApiKey) -> ApiKeyDbSchema:
        return ApiKeyDbSchema(
            id=api_key.id,
            user_id=api_key.user_id,
            key_name=api_key.key_name,
            key_hash=api_key.key_hash,
            key_prefix=api_key.key_prefix,
            created_at=api_key.created_at,
            last_used_at=api_key.last_used_at,
            expires_at=api_key.expires_at,
        )

    @staticmethod
    def to_domain(db_schema: ApiKeyDbSchema) -> ApiKey:
        return ApiKey(
            id=cast(Optional[str], db_schema.id),
            user_id=cast(str, db_schema.user_id),
            key_name=cast(str, db_schema.key_name),
            key_hash=cast(str, db_schema.key_hash),
            key_prefix=cast(str, db_schema.key_prefix),
            created_at=cast(Optional[datetime], db_schema.created_at),
            last_used_at=cast(Optional[datetime], db_schema.last_used_at),
            expires_at=cast(Optional[datetime], db_schema.expires_at),
        )
