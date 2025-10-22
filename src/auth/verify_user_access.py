from src.auth.validate_token import validate_token


from fastapi import HTTPException


def verify_user_access(token: str, requested_user_id: str) -> None:
    payload = validate_token(token)
    token_user_id = payload.get("user_id")

    if not token_user_id:
        raise HTTPException(status_code=401, detail="Invalid token: missing user information")

    if token_user_id != requested_user_id:
        raise HTTPException(status_code=403, detail="Access denied: cannot access other user's data")