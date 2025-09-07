#!/usr/bin/env python3
# filepath: /home/hfduran/progs/canaicode/scripts/manage_db.py
"""
Database management CLI script.
Usage:
    python scripts/manage_db.py init     # Initialize database (create tables)
    python scripts/manage_db.py drop     # Drop all tables (WARNING: destructive)
    python scripts/manage_db.py test     # Test database connection
    python scripts/manage_db.py status   # Show database status and record counts
    python scripts/manage_db.py clear    # Clear all data (keep tables)
    python scripts/manage_db.py sample   # Show sample data from tables
"""

import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def show_database_status() -> None:
    """Show the current status of the database."""
    from src.infrastructure.database.connection.database_connection import SessionLocal
    from src.infrastructure.database.raw_commit_metrics.postgre.dtos.model import RawCommitMetrics
    from src.infrastructure.database.raw_copilot_code_metrics.postgre.dtos.model import RawCopilotCodeMetrics
    from src.infrastructure.database.raw_copilot_chat_metrics.postgre.dtos.model import RawCopilotChatMetrics
    from src.infrastructure.database.users.postgre.dtos.model import UserDbSchema

    logger.info("Checking database status...")
    db = SessionLocal()
    try:
        commit_count = db.query(RawCommitMetrics).count()
        code_count = db.query(RawCopilotCodeMetrics).count()
        chat_count = db.query(RawCopilotChatMetrics).count()
        users_count = db.query(UserDbSchema).count()

        logger.info("Database status:")
        logger.info(f"  - Commit metrics: {commit_count} records")
        logger.info(f"  - Copilot code metrics: {code_count} records")
        logger.info(f"  - Copilot chat metrics: {chat_count} records")
        logger.info(f"  - Users: {users_count} records")
        logger.info(f"  - Total records: {commit_count + code_count + chat_count + users_count}")

    except Exception as e:
        logger.error(f"Error checking database status: {e}")
        raise
    finally:
        db.close()


def clear_all_data() -> None:
    """Clear all data from the database."""
    from src.infrastructure.database.connection.database_connection import SessionLocal
    from src.infrastructure.database.raw_commit_metrics.postgre.dtos.model import RawCommitMetrics
    from src.infrastructure.database.raw_copilot_code_metrics.postgre.dtos.model import RawCopilotCodeMetrics
    from src.infrastructure.database.raw_copilot_chat_metrics.postgre.dtos.model import RawCopilotChatMetrics
    from src.infrastructure.database.users.postgre.dtos.model import UserDbSchema

    logger.info("Clearing all data from database...")
    db = SessionLocal()
    try:
        db.query(RawCopilotChatMetrics).delete()
        db.query(RawCopilotCodeMetrics).delete()
        db.query(RawCommitMetrics).delete()
        db.query(UserDbSchema).delete()
        db.commit()
        logger.info("All data cleared successfully!")
    except Exception as e:
        logger.error(f"Error clearing data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def show_sample_data(limit: int = 5) -> None:
    """Show sample data from each table."""
    from src.infrastructure.database.connection.database_connection import SessionLocal
    from src.infrastructure.database.raw_commit_metrics.postgre.dtos.model import RawCommitMetrics
    from src.infrastructure.database.raw_copilot_code_metrics.postgre.dtos.model import RawCopilotCodeMetrics
    from src.infrastructure.database.raw_copilot_chat_metrics.postgre.dtos.model import RawCopilotChatMetrics
    
    logger.info(f"Showing sample data (limit: {limit})...")
    db = SessionLocal()
    try:
        # Show sample commit metrics
        commits = db.query(RawCommitMetrics).limit(limit).all()
        if commits:
            logger.info("Sample commit metrics:")
            for commit in commits:
                logger.info(f"  {commit.date.date()} | {commit.repository_team} | "
                          f"{commit.author_name} | {commit.language} | "
                          f"+{commit.added_lines}/-{commit.removed_lines}")
        
        # Show sample code metrics
        code_metrics = db.query(RawCopilotCodeMetrics).limit(limit).all()
        if code_metrics:
            logger.info("Sample Copilot code metrics:")
            for metric in code_metrics:
                logger.info(f"  {metric.date.date()} | {metric.team_name} | "
                          f"{metric.ide} | {metric.total_users} users | "
                          f"{metric.code_acceptances}/{metric.code_suggestions} suggestions")
        
        # Show sample chat metrics
        chat_metrics = db.query(RawCopilotChatMetrics).limit(limit).all()
        if chat_metrics:
            logger.info("Sample Copilot chat metrics:")
            for metric in chat_metrics:
                logger.info(f"  {metric.date.date()} | {metric.team_name} | "
                          f"{metric.ide} | {metric.total_users} users | "
                          f"{metric.total_chats} chats")
    except Exception as e:
        logger.error(f"Error showing sample data: {e}")
        raise
    finally:
        db.close()


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        # Import modules inside the function to avoid module-level import issues
        from src.infrastructure.database.init_db import init_database, drop_tables
        from src.infrastructure.database.database_utils import test_database_connection
        
        if command == 'init':
            logger.info("Initializing database...")
            init_database()
            logger.info("Database initialized successfully!")
            
        elif command == 'drop':
            response = input("Are you sure you want to drop all tables? This will delete all data! (yes/no): ")
            if response.lower() == 'yes':
                logger.warning("Dropping all tables...")
                drop_tables()
                logger.warning("All tables dropped!")
            else:
                logger.info("Operation cancelled.")
                
        elif command == 'test':
            logger.info("Testing database connection...")
            if test_database_connection():
                logger.info("Database connection test passed!")
            else:
                logger.error("Database connection test failed!")
                sys.exit(1)
                
        elif command == 'status':
            show_database_status()
            
        elif command == 'clear':
            response = input("Are you sure you want to clear all data? Tables will be kept. (yes/no): ")
            if response.lower() == 'yes':
                clear_all_data()
            else:
                logger.info("Operation cancelled.")
                
        elif command == 'sample':
            show_sample_data()
                
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error executing command '{command}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
