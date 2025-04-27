from pydantic import BaseModel


class Entity(BaseModel):
    id: str | None = None
