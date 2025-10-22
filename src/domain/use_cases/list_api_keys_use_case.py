from typing import List

from src.domain.entities.api_key import ApiKey
from src.infrastructure.database.api_keys.postgre.api_keys_repository import ApiKeysRepository


class ListApiKeysUseCase:
    def __init__(self, api_keys_repository: ApiKeysRepository) -> None:
        self.api_keys_repository = api_keys_repository

    def execute(self, user_id: str) -> List[ApiKey]:
        """
        List all API keys for a user.
        Note: The key_hash should not be exposed in the API response.
        """
        return self.api_keys_repository.find_by_user_id(user_id)
