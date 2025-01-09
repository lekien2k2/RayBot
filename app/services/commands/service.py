from datetime import datetime
import logging
from typing import Callable, Optional

from app.services.commands.schemas import CommandReceiveSchema, CommandStatusEnum
from app.services.api.logs import service as log_service
from app.services.api.logs.schemas import CreateLogSchema
from sqlalchemy.orm import Session
from app.database.sqlite.db import SessionLocal

logger = logging.getLogger(__name__)


class CommandStatus:
    def __init__(self):
        self.command: dict = {}
        self.callback_on_new = None

    def add_callback_on_new(self, callback: Callable):
        logger.info(f"Callback on new command: {callback}")
        self.callback_on_new = callback

    def add_command(self, command: CommandReceiveSchema, callback: Callable = None):
        logger.info(f"Command: {command.model_dump()}")
        self.command = {
            "status": CommandStatusEnum.IN_PROGRESS,
            "name": command.type,
            "callback": callback,
            "command": command.model_dump(),
        }
        logger.info("ASDSSAD")
        # log = CreateLogSchema(
        #     username="system",
        #     action="command",
        #     time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #     status=CommandStatusEnum.IN_PROGRESS,
        #     message=f"Command {command.type} received",
        # )
        # logger.info(f"logs: {log}")
        # db: Session = SessionLocal()
        # log_service.create_log(db, log)
        logger.info(f"Command: {command}")
        self.callback_on_new(command)

    def update_status(self, command_id: str, status: str, msg: dict = None):
        self.command["status"] = status
        logger.info(f"Command {command_id} status: {status} in update_status")
        # log = CreateLogSchema(
        #     username="system",
        #     action="command",
        #     time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #     status=status,
        #     message=msg,
        # )
        if self.command.get("callback"):
            logger.info(f"Callback: {self.command['callback']}")
            self.command["callback"](command_id, self.command["name"], status, msg)

    def get_command_status(self, command_id: str) -> Optional[dict]:
        return self.commands.get(command_id)

    def get_current_command(self) -> Optional[dict]:
        return self.command


# Example usage
command_manager = CommandStatus()
