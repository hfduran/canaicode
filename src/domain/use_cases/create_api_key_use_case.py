import secrets
import string
import uuid
from datetime import datetime, timezone
from typing import Optional
from passlib.context import CryptContext

from src.domain.entities.api_key import ApiKey
from src.infrastructure.database.api_keys.postgre.api_keys_repository import ApiKeysRepository


class CreateApiKeyUseCase:
    def __init__(self, api_keys_repository: ApiKeysRepository) -> None:
        self.api_keys_repository = api_keys_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def execute(
        self,
        user_id: str,
        key_name: str,
        expires_at: Optional[datetime] = None
    ) -> tuple[str, ApiKey]:
        """
        Create a new API key for a user.
        Returns: (full_key_plaintext, api_key_entity)
        The plaintext key is only returned once and never stored.
        """
        # Generate cryptographically secure random key
        # Format: cak_<40 random chars> = total 44 chars
        random_part = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(40)
        )
        full_key = f"cak_{random_part}"

        # Extract prefix (first 15 chars for lookup optimization)
        key_prefix = full_key[:15]

        # Hash the full key
        key_hash = self.pwd_context.hash(full_key)  # type: ignore

        # Create entity
        api_key = ApiKey(
            id=str(uuid.uuid4()),
            user_id=user_id,
            key_name=key_name,
            key_hash=key_hash,
            key_prefix=key_prefix,
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at,
        )

        # Save to database
        self.api_keys_repository.create(api_key)

        # Return plaintext key (only shown once!) and entity
        return full_key, api_key
