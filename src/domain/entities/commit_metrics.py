from datetime import datetime

from src.domain.entities.author import Author
from src.domain.entities.entity import Entity
from src.domain.entities.repository import Repository


class CommitMetrics(Entity):
    hash: str
    repository: Repository
    date: datetime
    author: Author
    language: str
    added_lines: int
    removed_lines: int
