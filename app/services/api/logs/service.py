from app.database.sqlite.models.logs import Logs

from app.services.api.logs.schemas import CreateLogSchema
from sqlalchemy.orm import Session


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
