from datetime import datetime
from typing import Optional
from src.domain.entities.entity import Entity


class User(Entity):
    username: str
    hashed_password: str
    full_name: str
    enterprise_name: Optional[str] = None
    email: str
    cellphone: str
    cpf_cnpj: str
    created_at: Optional[datetime] = None