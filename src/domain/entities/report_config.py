from datetime import datetime
from typing import List, Optional
from src.domain.entities.entity import Entity
from src.domain.entities.value_objects.enums.period import Period


class ReportConfig(Entity):
  emails: List[str]
  period: Period
  user_id: str
  created_at: Optional[datetime] = None