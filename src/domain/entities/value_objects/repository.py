from pydantic import BaseModel


class Repository(BaseModel):
    name: str
    team: str  # mudar para Team
