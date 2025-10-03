from typing import Optional
from pydantic import BaseModel


class Repository(BaseModel):
    id: Optional[str] = None
    name: str
    team: str  # mudar para Team
