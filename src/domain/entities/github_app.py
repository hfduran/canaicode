from datetime import datetime
from typing import Optional
from src.domain.entities.entity import Entity


class GitHubApp(Entity):
  organization_name: str
  app_id: str
  installation_id: str
  private_key_encrypted: str
  user_id: str
  created_at: Optional[datetime] = None