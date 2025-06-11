#!/usr/bin/env python3
# filepath: /home/hfduran/progs/canaicode/scripts/manage_db.py
"""
Database management CLI script.
Usage:
    python scripts/manage_db.py init     # Initialize database (create tables)
    python scripts/manage_db.py drop     # Drop all tables (WARNING: destructive)
    python scripts/manage_db.py test     # Test database connection
"""

import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
                
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error executing command '{command}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
