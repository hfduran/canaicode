import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    error_msg = (
        "DATABASE_URL environment variable is not set!\n"
        "Please create a .env file in the project root with:\n"
        "DATABASE_URL=postgresql://username:password@host:port/database\n"
        "Example: DATABASE_URL=postgresql://user:pass@localhost:5432/mydb"
    )
    print(error_msg, file=sys.stderr)
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
