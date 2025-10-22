from typing import Optional
from fastapi import Header, HTTPException

from src.auth.validate_api_key import validate_api_key
from src.auth.validate_token import validate_token


def get_user_id_dual_auth(
    x_api_key: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
) -> str:
    """
    Dual authentication: accepts either API key or JWT token.

    Priority:
    1. X-API-Key header - if present, validate as API key
    2. Authorization header - if present, validate as JWT Bearer token
    3. If neither present, raise 401

    Returns the user_id extracted from the authentication method used.
    """
    # Try API key first
    if x_api_key:
        user_id = validate_api_key(x_api_key)
        return user_id

    # Try JWT Bearer token
    if authorization:
        # Extract Bearer token
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization header format. Expected: 'Bearer <token>'"
            )

        token = parts[1]
        payload = validate_token(token)
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user information"
            )

        return user_id  # type: ignore

    # No authentication provided
    raise HTTPException(
        status_code=401,
        detail="Authentication required. Provide either X-API-Key or Authorization Bearer token."
    )
