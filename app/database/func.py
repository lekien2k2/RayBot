import hashlib
import logging
from datetime import datetime, timedelta
from time import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.sqlite import models  # noqa
from app.database.sqlite.base import BaseModel
from app.database.sqlite.db import engine

from app.database.sqlite.models.user import User

logger = logging.getLogger(__name__)


def convert_datetime_to_local_time(dt: datetime) -> str:
    """
    Convert datetime to local time
    """
    local_dt = dt + timedelta(hours=7)
    return local_dt.strftime("%Y-%m-%dT%H:%M:%S")


def hash_password(password: str) -> str:
    pw_bytes = password.encode("utf-8")
    hashed_pw = hashlib.sha256(pw_bytes).hexdigest()
    return hashed_pw


def check_db():
    """Check if the database is empty and insert default values if it is."""
    start_time = time()
    with Session(engine) as db:
        BaseModel.metadata.create_all(engine)
        acc_exists = db.execute(select(User.id)).scalars().all()
        if not acc_exists:
            root_acc = User(
                username="root", password=hash_password("1234"), is_active=True
            )
            new_account = User(
                username="admin", password=hash_password("1234"), is_active=True
            )
            db.add(root_acc)
            db.add(new_account)

            db.commit()

    logger.info(f"Database check took {time() - start_time} seconds")

