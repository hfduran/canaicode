from typing import List, Optional

from pydantic import BaseModel


class Author(BaseModel):
    name: Optional[str]
    teams: List[str]
