from typing import Optional
from app.database.sqlite.models.logs import Logs

from app.services.api.logs.schemas import CreateLogSchema
from sqlalchemy.orm import Session
from app.services.api.utils import build_meta_data


def create_log(db: Session, log: CreateLogSchema):
    new_log = Logs(
        username=log.username,
        action=log.action,
        time=log.time,
        status=log.status,
        message=log.message,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


def get_logs(
    db: Session,
    *,
    page: int,
    limit: int,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    sort_order: str,
):
    query = db.query(Logs)
    if from_date:
        query = query.filter(Logs.time >= from_date)
    if to_date:
        query = query.filter(Logs.time <= to_date)
    if sort_order == "asc":
        query = query.order_by(Logs.id.asc())
    else:
        query = query.order_by(Logs.id.desc())
    logs = query.offset((page - 1) * limit).limit(limit).all()
    return logs, build_meta_data(page=page, limit=limit, total_count=query.count())
