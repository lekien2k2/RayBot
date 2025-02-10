from datetime import datetime
import logging
from typing import Callable, Optional

from app.services.commands.schemas import CommandReceiveSchema, CommandStatusEnum
from app.services.api.logs import service as log_service
from app.services.api.logs.schemas import CreateLogSchema
from app.services.api.command.schemas import CommandUpdateSchema, CreateCommandSchema
from app.services.api.command import service as command_service
from sqlalchemy.orm import Session
from app.database.sqlite.db import session_scope
import uuid

logger = logging.getLogger(__name__)


class CommandStatus:
    def __init__(self):
        self.command: dict = {}
        self.callback_on_new = None

    def add_callback_on_new(self, callback: Callable):
        logger.info(f"Callback on new command: {callback}")
        self.callback_on_new = callback

    def add_command(
        self,
        command: CommandReceiveSchema,
        callback: Callable = None,
        mode: str = "server_side",
    ):
        logger.info(f"Command: {command.model_dump()}")
        self.command = {
            "status": CommandStatusEnum.IN_PROGRESS,
            "name": command.type,
            "callback": callback,
            "command": command.model_dump(),
        }
        logger.info("ASDSSAD")
        log = CreateLogSchema(
            username="system",
            action="command",
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status=CommandStatusEnum.PENDING,
            message=f"Command {command.type} received",
        )
        c = CreateCommandSchema(
            id=command.id,
            type=command.type,
            status=CommandStatusEnum.PENDING,
            data=command.data,
            mode=mode,
        )
        logger.info(f"logs: {log}")
        with session_scope() as session:
            log_service.create_log(session, log)
            command_service.create_command(session, c)
        logger.info(f"Command: {command}")
        self.callback_on_new(command)

    def update_status(self, command_id: str, status: str, msg: dict = None):
        self.command["status"] = status
        logger.info(f"Command {command_id} status: {status} in update_status")
        log = CreateLogSchema(
            username="system",
            action="command",
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status=status,
        )
        command = CommandUpdateSchema(
            status=status,
            data=msg,
        )
        # command_id = uuid.UUID(command_id)
        with session_scope() as session:
            command_service.update_command(session, uuid.UUID(command_id), command)
            log_service.create_log(session, log)
        if self.command.get("callback"):
            logger.info(f"Callback: {self.command['callback']}")
            self.command["callback"](command_id, self.command["name"], status, msg)

    def get_command_status(self, command_id: str) -> Optional[dict]:
        return self.commands.get(command_id)

    def get_current_command(self) -> Optional[dict]:
        return self.command


# Example usage
command_manager = CommandStatus()
