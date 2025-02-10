from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm.session import Session

from app.database.sqlite.db import SessionLocal


def get_db() -> Generator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_db)]
