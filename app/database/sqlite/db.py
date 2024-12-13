from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager

from app.constants import SQLITE_DB_PATH

DB_PATH = SQLITE_DB_PATH

engine = create_engine(
    DB_PATH,
    echo=False,
    connect_args={"check_same_thread": False, "timeout": 15},
)


SessionLocal = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()  # Use SessionLocal instead of Session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
