from fastapi import HTTPException

from src.infrastructure.database.api_keys.postgre.api_keys_repository import ApiKeysRepository


class RevokeApiKeyUseCase:
    def __init__(self, api_keys_repository: ApiKeysRepository) -> None:
        self.api_keys_repository = api_keys_repository

    def execute(self, user_id: str, key_id: str) -> None:
        """
        Revoke (delete) an API key.
        Verifies that the key belongs to the user before deletion.
        """
        # Verify the key exists and belongs to this user
        api_key = self.api_keys_repository.find_by_id(key_id)

        if not api_key:
            raise HTTPException(status_code=404, detail="API key not found")

        if api_key.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Cannot revoke another user's API key"
            )

        # Delete the key
        self.api_keys_repository.delete(key_id)
