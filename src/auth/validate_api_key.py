from src.cmd.dependencies.dependency_setters import set_validate_api_key_dependencies
from src.infrastructure.database.connection.database_connection import SessionLocal


def validate_api_key(api_key: str) -> str:
    """
    Validate an API key and return the user_id.
    Raises HTTPException if invalid.
    """
    db = SessionLocal()
    try:
        validate_api_key_use_case = set_validate_api_key_dependencies(db)
        user_id = validate_api_key_use_case.execute(api_key)
        return user_id
    finally:
        db.close()
