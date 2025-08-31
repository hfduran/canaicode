from pydantic import BaseModel


class Token(BaseModel):
    user_id: str
    access_token: str
    token_type: str