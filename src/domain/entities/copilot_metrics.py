from datetime import datetime

from src.domain.entities.entity import Entity


class CopilotMetrics(Entity):
    team: str
    date: datetime
    IDE: str
    copilot_model: str
