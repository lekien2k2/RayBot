from app.database.sqlite.models.command import Command

from app.services.api.command.schemas import CreateCommandSchema, CommandUpdateSchema
from sqlalchemy.orm import Session
from app.services.api.utils import build_meta_data


def create_command(db: Session, command: CreateCommandSchema):
    new_command = Command(**command.model_dump())
    db.add(new_command)
    db.commit()
    db.refresh(new_command)
    return new_command


def update_command(db: Session, id: int, request: CommandUpdateSchema):
    command = db.query(Command).filter(Command.id == id).first()
    for key, value in request.model_dump().items():
        setattr(command, key, value)
    db.commit()
    db.refresh(command)
    return command


def get_commands(
    db: Session,
    *,
    page: int,
    limit: int,
    from_date: str,
    to_date: str,
    sort_order: str,
):
    query = db.query(Command)
    if from_date:
        query = query.filter(Command.time >= from_date)
    if to_date:
        query = query.filter(Command.time <= to_date)
    if sort_order == "asc":
        query = query.order_by(Command.created_at.asc())
    else:
        query = query.order_by(Command.created_at.desc())
    commands = query.offset((page - 1) * limit).limit(limit).all()
    return commands, build_meta_data(page=page, limit=limit, total_count=query.count())
