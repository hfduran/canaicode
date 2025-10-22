import os


from fastapi import HTTPException
from jose import JWTError, jwt


from typing import Any, Dict

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def validate_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        return payload # type: ignore
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")