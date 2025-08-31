from datetime import datetime
from typing import Optional
from src.domain.entities.entity import Entity


class User(Entity):
    username: str
    hashed_password: str
    created_at: Optional[datetime] = None