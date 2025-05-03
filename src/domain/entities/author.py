from src.domain.entities.entity import Entity
from typing import List

class Author(Entity):
    name: str
    teams: List[str]
