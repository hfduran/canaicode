from datetime import datetime
from typing import Optional

from src.domain.entities.entity import Entity
from src.domain.entities.value_objects.author import Author
from src.domain.entities.value_objects.repository import Repository


class CommitMetrics(Entity):
    hash: str
    repository: Repository
    date: datetime
    author: Author
    language: str
    added_lines: int
    removed_lines: int
    created_at: Optional[datetime] = None
