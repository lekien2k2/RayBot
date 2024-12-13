# QR Code Generator Simulation
import random
import threading
import time
from queue import Queue
from typing import Any

from loguru import logger

from ..app.types import CommandType, InboundCommand


class QRCodeGenerator:
    def __init__(self, fake_qr_codes: list[str]):
        self.fake_qr_codes = fake_qr_codes
        self.queue: Queue[str] = Queue()
        self.is_moving = False

        self._start_generator()

    def _start_generator(self):
        def generate():
            while True:
                if self.is_moving:
                    qr_code = random.choice(self.fake_qr_codes)
                    logger.debug(f"Generate QR code: {qr_code}")
                    self.queue.put(qr_code)
                    # Random delay to simulate real-world scenario
                    time.sleep(random.randint(1, 5))
                time.sleep(0.001)

        thread = threading.Thread(target=generate, daemon=True)
        thread.start()

    def set_moving(self, is_moving: bool):
        self.is_moving = is_moving


class CommandGenerator:
    def __init__(self, fake_qr_codes: list[str]):
        self.fake_qr_codes = fake_qr_codes
        self.command_queue: Queue[InboundCommand] = Queue()
        self.counter = 0

        self._start_generator()

    def _start_generator(self):
        def generate():
            # while True:
            # command = random.choice(list(CommandType))
            command = CommandType.GO_FORWARD
            self._create_command(command)
            time.sleep(5)

        threading.Thread(target=generate, daemon=True).start()

    def _create_command(self, command: CommandType) -> None:
        """Generate and enqueue a command based on the command type."""
        has_destination = (
            random.choice([True, False])
            if command in [CommandType.GO_FORWARD, CommandType.GO_BACKWARD]
            else False
        )
        destination = random.choice(self.fake_qr_codes) if has_destination else None
        data: dict[str, Any] = {"destination_qr": destination} if destination else {}

        self.counter += 1
        self.command_queue.put(InboundCommand(str(self.counter), command, data))

        action = {
            CommandType.GO_FORWARD: "moving forward",
            CommandType.GO_BACKWARD: "moving backward",
            CommandType.SCAN_QR_CODE: "scanning QR code",
            CommandType.STOP: "stopped",
        }.get(command, "unknown command")

        if destination:
            logger.debug(f"Create command {action} to {destination}")
        else:
            logger.debug(f"Create command {action}")
