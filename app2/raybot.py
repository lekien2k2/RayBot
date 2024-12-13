import threading
import time
from queue import Queue
from typing import Any

from loguru import logger

from app.types import (
    CommandStatus,
    CommandType,
    InboundCommand,
    MovementState,
    OutboundCommand,
)

from ..app.notifier import EventNotifier
from .generator import CommandGenerator, QRCodeGenerator

FAKE_QR_CODES = ["A1", "B2", "C3", "D4", "E5"]


class WebSocketResponseHandler:
    def handle(self, cmd: OutboundCommand):
        logger.debug(f"Receive webSocket response - Command {cmd.id}: {cmd.data}")


class Raybot(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.daemon = True

        # Fake Components
        self.qr_generator = QRCodeGenerator(FAKE_QR_CODES)
        self.command_generator = CommandGenerator(FAKE_QR_CODES)
        self.web_socket_response_handler = WebSocketResponseHandler()

        #  States
        self.current_qr_code: str | None = None
        self.movement_state: MovementState = MovementState.IDLE
        self.current_command: InboundCommand | None = None

        # Event Manager
        self.location_event_notifier = EventNotifier[str]()

        # Queues
        self.outbound_msg_queue: Queue[OutboundCommand] = Queue()

        self._start_handlers()

    def _start_handlers(self) -> None:
        handlers = [
            threading.Thread(target=self._handle_inbound_msg, daemon=True),
            threading.Thread(target=self._handle_outbound_msg, daemon=True),
            threading.Thread(target=self._handle_qr_tracking, daemon=True),
        ]
        for worker in handlers:
            worker.start()

    def _handle_outbound_msg(self) -> None:
        logger.info("Outbound message handler started")
        while True:
            if not self.outbound_msg_queue.empty():
                outbound_msg = self.outbound_msg_queue.get()

                # Fake sending message to WebSocket
                self.web_socket_response_handler.handle(outbound_msg)

            time.sleep(0.0001)

    def _handle_inbound_msg(self) -> None:
        logger.info("Inbound message handler started")

        # Because all message inbound received are command so we get directly from command generator
        while True:
            if not self.command_generator.command_queue.empty():
                command = self.command_generator.command_queue.get()

                # Suppose we already convert bytes to command object
                logger.info(f"Received new command: {command}")

                self._route_inbound_command(command)

            time.sleep(0.0001)

    def _handle_qr_tracking(self) -> None:
        """Only responsible for tracking current QR code"""
        logger.info("QR tracking handler started")
        while True:
            if not self.qr_generator.queue.empty():
                qr_code = self.qr_generator.queue.get()
                self.current_qr_code = qr_code
                logger.info(f"Current location: {qr_code}")

                # Notify to all subscribers
                self.location_event_notifier.dispatch(qr_code)

            time.sleep(0.0001)

    def _route_inbound_command(self, command: InboundCommand) -> None:
        # 1. Validate command can be executed or overrided

        # 2. Start executing command
        self.current_command = command
        self._notify_command_to_server(command.id, CommandStatus.IN_PROGRESS)

        # 3. Route command to specific handler
        if command.type in [CommandType.GO_FORWARD, CommandType.GO_BACKWARD]:
            self._handle_movement_command(command)
        elif command.type == CommandType.STOP:
            self._handle_stop_command(command)
        elif command.type == CommandType.SCAN_QR_CODE:
            self._handle_scan_command(command)

    def _handle_movement_command(self, command: InboundCommand) -> None:
        def movement_task() -> None:
            logger.debug("Start movement task")
            if command.type == CommandType.GO_FORWARD:
                self.movement_state = MovementState.FORWARD
            elif command.type == CommandType.GO_BACKWARD:
                self.movement_state = MovementState.BACKWARD

            # Just for generating QR code
            self.qr_generator.set_moving(True)

            # Do something with arduino

            # If no destination, just move forever
            destination_qr = command.data.get("destination_qr")
            if not destination_qr:
                self._notify_command_to_server(command.id, CommandStatus.SUCCESS)
            else:
                # Listen to location event
                queue = self.location_event_notifier.create_queue_listener()
                while True:
                    if not queue.empty():
                        if queue.get() == destination_qr:
                            logger.debug("Reached destination")
                            self._notify_command_to_server(
                                command.id, CommandStatus.SUCCESS
                            )
                            break
                    time.sleep(0.001)

                self.location_event_notifier.remove_queue_listener(queue)

            self.movement_state = MovementState.IDLE

            # Just for generating QR code
            self.qr_generator.set_moving(False)

        thread = threading.Thread(target=movement_task, daemon=True)
        thread.start()

    def _handle_stop_command(self, command: InboundCommand) -> None:
        self.movement_state = MovementState.IDLE
        self.qr_generator.set_moving(False)

        self._notify_command_to_server(command.id, CommandStatus.SUCCESS)

    def _handle_scan_command(self, command: InboundCommand) -> None:
        def scan_task() -> None:
            # SCAN_TIMEOUT = 10
            # start_time = time.time()

            # while time.time() - start_time < SCAN_TIMEOUT:
            #     # TODO: Need to handle QR code tracking
            #     # Wrong algorithm
            #     if self.current_qr_code == command.data["destination_qr"]:
            #         # TODO: Need to handle send all collected commands to server
            #         self._notify_command_to_server(command.id, CommandStatus.SUCCESS)
            #         return

            #     time.sleep(0.001)

            tracked_qr: list[str] = []

            # Just for generating QR code
            self.qr_generator.set_moving(True)

            # Listen to location event
            queue = self.location_event_notifier.create_queue_listener()
            while True:
                if not queue.empty():
                    qr_code = queue.get()
                    logger.debug(f"Tracked QR code: {qr_code}")

                    # We need to track if the destination QR code is found then append to qr_tracked until duplicate
                    # When duplicate so robot is run full circle that means it scanned all QR codes
                    if qr_code in tracked_qr:
                        logger.debug(
                            f"Completed full circuit! QR code {qr_code} seen twice"
                        )
                        break

                time.sleep(0.001)

            # Just for generating QR code
            self.qr_generator.set_moving(False)

            self.location_event_notifier.remove_queue_listener(queue)

            self._notify_command_to_server(command.id, CommandStatus.ERROR)

        thread = threading.Thread(target=scan_task, daemon=True)
        thread.start()

    def _notify_command_to_server(
        self, cmd_id: str, status: CommandStatus, data: dict[str, Any] | None = None
    ) -> None:
        self.outbound_msg_queue.put(
            OutboundCommand(
                id=cmd_id,
                data={"status": status, "data": data} if data else {"status": status},
            )
        )
