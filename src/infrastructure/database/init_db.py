import logging
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.database.connection.database_connection import Base, engine

# Import all models to ensure they are registered with the Base metadata
from src.infrastructure.database.raw_copilot_code_metrics.postgre.dtos.model import RawCopilotCodeMetrics  # noqa: F401
from src.infrastructure.database.raw_copilot_chat_metrics.postgre.dtos.model import RawCopilotChatMetrics  # noqa: F401
from src.infrastructure.database.raw_commit_metrics.postgre.dtos.model import RawCommitMetrics  # noqa: F401

logger = logging.getLogger(__name__)


def create_tables() -> None:
    """
    Create all database tables defined in the models.
    This function should be called once when the application starts.
    """
    try:
        logger.info("Creating database tables...")
        # This will create all tables that don't exist yet
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
        # Log the tables that were registered
        table_names = [table.name for table in Base.metadata.tables.values()]
        logger.info(f"Registered tables: {', '.join(table_names)}")
        
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        raise


def drop_tables() -> None:
    """
    Drop all database tables. Use with caution!
    This is typically used for testing or resetting the database.
    """
    try:
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped!")
    except SQLAlchemyError as e:
        logger.error(f"Error dropping database tables: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database cleanup: {e}")
        raise


def init_database() -> None:
    """
    Initialize the database by creating all tables.
    This is the main function to call for database setup.
    """
    create_tables()


if __name__ == "__main__":
    # Allow running this script directly for manual database initialization
    logging.basicConfig(level=logging.INFO)
    init_database()
