from datetime import datetime, timezone
from fastapi import HTTPException
from passlib.context import CryptContext

from src.infrastructure.database.api_keys.postgre.api_keys_repository import ApiKeysRepository


class ValidateApiKeyUseCase:
    def __init__(self, api_keys_repository: ApiKeysRepository) -> None:
        self.api_keys_repository = api_keys_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def execute(self, api_key: str) -> str:
        """
        Validate an API key and return the user_id.
        Raises HTTPException if key is invalid or expired.
        """
        # Extract prefix (first 15 chars: "cak_" + 11 chars)
        if len(api_key) < 15:
            raise HTTPException(status_code=401, detail="Invalid API key format")

        key_prefix = api_key[:15]

        # Find all keys with this prefix
        potential_keys = self.api_keys_repository.find_by_prefix(key_prefix)

        if not potential_keys:
            raise HTTPException(status_code=401, detail="Invalid API key")

        # Try to verify the hash against each potential key
        for key_record in potential_keys:
            if self.pwd_context.verify(api_key, key_record.key_hash):  # type: ignore
                # Check if expired
                if key_record.expires_at and key_record.expires_at < datetime.now(timezone.utc):
                    raise HTTPException(status_code=401, detail="API key has expired")

                # Update last_used_at
                self.api_keys_repository.update_last_used(
                    key_record.id,  # type: ignore
                    datetime.now(timezone.utc)
                )

                return key_record.user_id

        # No matching hash found
        raise HTTPException(status_code=401, detail="Invalid API key")
