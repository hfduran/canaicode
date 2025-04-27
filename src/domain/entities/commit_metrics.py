from datetime import datetime

from src.domain.entities.entity import Entity


class CommitMetrics(Entity):
    hash: str
    repository: str
    date: datetime
    author: str
    language: str
    added_lines: int
    removed_lines: int
