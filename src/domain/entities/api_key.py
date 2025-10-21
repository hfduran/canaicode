from datetime import datetime
from typing import Optional
from src.domain.entities.entity import Entity


class ApiKey(Entity):
    user_id: str
    key_name: str
    key_hash: str
    key_prefix: str
    created_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
