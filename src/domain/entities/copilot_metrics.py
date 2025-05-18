from datetime import datetime
from typing import Optional

from src.domain.entities.entity import Entity
from src.domain.entities.value_objects.team import Team


class CopilotMetrics(Entity):
    team: Team
    date: datetime
    IDE: str
    copilot_model: str
    created_at: Optional[datetime] = None
