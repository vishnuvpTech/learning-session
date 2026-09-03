"""
Database engine and session setup.

Uses SQLite by default (network_backup.db in the project root) so the
project runs with zero external setup. Swap DATABASE_URL for a Postgres/
MySQL connection string in production without changing any other code.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./network_backup.db"

# check_same_thread=False is required for SQLite when used with FastAPI's
# threaded request handling / Nornir's threaded runner.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
