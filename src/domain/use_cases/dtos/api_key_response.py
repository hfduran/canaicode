from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ApiKeyResponse(BaseModel):
    """Response when creating a new API key - includes full plaintext key"""
    id: str
    key: str  # Full plaintext key - only shown once!
    key_name: str
    created_at: datetime
    expires_at: Optional[datetime] = None


class ApiKeyListItem(BaseModel):
    """Response when listing API keys - shows masked key"""
    id: str
    key_prefix: str  # Masked display like "cak_abc...xyz"
    key_name: str
    created_at: datetime
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
