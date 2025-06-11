import logging
from typing import Generator
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from src.infrastructure.database.connection.database_connection import SessionLocal

logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    This is typically used with FastAPI's dependency injection system.
    
    Usage:
        @app.get("/some-endpoint")
        def some_endpoint(db: Session = Depends(get_db)):
            # Use db session here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """
    Get a database session for direct use (not as a dependency).
    Remember to close the session when done!
    
    Usage:
        db = get_db_session()
        try:
            # Use db session here
            pass
        finally:
            db.close()
    """
    return SessionLocal()


def test_database_connection() -> bool:
    """
    Test the database connection.
    Returns True if connection is successful, False otherwise.
    """
    try:
        db = SessionLocal()
        # Execute a simple query to test the connection
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
