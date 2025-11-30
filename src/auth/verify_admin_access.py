import os

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()
ADMIN_KEY = os.getenv("ADMIN_KEY")

def verify_admin_access(token: str) -> None:
    if token != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Token invalid")
        
    return
