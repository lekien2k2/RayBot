import logging
import threading
from threading import Thread
from time import sleep
from typing import Optional
import re

import serial

# from app.config import serial_config

# from app.services.qr_service.service import qr_code_data
from app.schemas import SerialSchemas
from app.services.raybot.schemas import (
    CommandActionEnum,
    CommandEnum,
    DataCommandEnum,
    RayBotInfoSchema,
    RaybotConfigSchema,
    ReciveDataSchema,
)
from app.services.websockets.schemas import CommandReciveSchema

from app.services.commands.schemas import CommandStatusEnum
from app.services.commands.service import command_manager
from app.config import config_service
from app.services.audio import speak

logger = logging.getLogger(__name__)


class RaybotService(Thread):
    def __init__(self, serial_config: SerialSchemas, raybot_config: RaybotConfigSchema):
        Thread.__init__(self)
        self.daemon = True
        # self.serial1 = config_service.get_config(section="Robot-config")
        # logger.info(f"{self.serial1}")
        self.serial = serial.Serial(
            port=serial_config.port,
            baudrate=serial_config.baudrate,
            timeout=serial_config.timeout,
        )
        self.raybot_info = RayBotInfoSchema(
            max_distance_lift=raybot_config.max_distance_lift,
            min_distance_move=raybot_config.min_distance_move,
            min_distance_lift=raybot_config.min_distance_lift,
            max_pwm_movement=raybot_config.max_pwm_movement,
            max_pwm_lift=raybot_config.max_pwm_lift,
            home_location=raybot_config.home_location,
            current_cmd="",
            forward_distance=0,
            backward_distance=0,
            lift_distance=0,
            weight=0,
            movement_pwm=0,
            battery=0,
            movement_motor=0,
            lift_motor=0,
            lift_pwm=0,
            safety=False,
            door_state=0,
            qr_location="",
            qr_door="",
        )
        command_manager.add_callback_on_new(self.execute_command)
        self.command_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.lock = (
            threading.Lock()
        )  # Lock để tránh trường hợp hai lệnh được gọi đồng thời
        self.serial_lock = threading.Lock()
        self.commands = {
            "move_forward": self.handle_move_forward,
            "move_backward": self.handle_move_backward,
            "move_to_location": self.handle_move_to_location,
            "drop_box": self.handle_drop_box,
            "lift_box": self.handle_lift_box,
            "open_box": self.handle_open_box,
            "close_box": self.handle_close_box,
            "check_qr": self.handle_check_qr,
            "scan_location": self.handle_scan_location,
            "stop": self.handle_stop,
            "wait_get_item": self.handle_wait_get_item,
            "speak": self.handle_speak,
        }

    def send(self, data):
        try:
            self.serial.write(data)
            logger.info(f"Sent: {data}")
        except Exception as e:
            logger.error(f"Error: {e}")

    def send_command(self, command: str, data: Optional[str] = None) -> bool:
        # Thử lấy khóa
        if not self.serial_lock.acquire(timeout=5):  # Timeout để tránh deadlock
            logger.error("Unable to acquire lock, another thread is sending.")
            return False

        try:
            if data:
                logger.info(f"Send command: {command} with data: {data}")
                self.send(f"CMD:{command}\n".encode())
                self.send(f"DATA:{data}\n".encode())
                self.raybot_info.current_cmd = command  # TEST
            else:
                logger.info(f"Send command: {command}")
                self.send(f"CMD:{command}\n".encode())
                self.raybot_info.current_cmd = command
            sleep(0.05)  # Đảm bảo chỉ mình nó gửi trong thời gian này
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
        finally:
            self.serial_lock.release()  # Nhả khóa sau khi xong

    def send_data(self, data: dict) -> bool:
        # Thử lấy khóa
        if not self.serial_lock.acquire(timeout=5):  # Timeout để tránh deadlock
            logger.error("Unable to acquire lock, another thread is sending.")
            return False

        try:
            self.send(f"DATA:{data}\n".encode())
            logger.info(f"Sent data: {data}")
            sleep(0.05)  # Đảm bảo chỉ mình nó gửi trong thời gian này
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
        finally:
            self.serial_lock.release()  # Nhả khóa sau khi xong

    def _handle_recive_data(self, data):
        try:
            # logger.info(f"Recive data: {data}")
            if data.startswith("DATA:"):
                # Tách giá trị sau "DATA:"
                value = data.split(":", 1)[1]
                # logger.info(f"Recive raw value: {value}")

                # Tiền xử lý dữ liệu để chuẩn hóa JSON
                fixed_value = value.replace("'", '"')  # Thay ' bằng "
                if not fixed_value.strip().startswith("{"):
                    fixed_value = "{" + fixed_value
                if not fixed_value.strip().endswith("}"):
                    fixed_value = fixed_value + "}"

                # logger.info(f"Fixed value: {fixed_value}")
                fixed_value = self._sanitize_serial_data(fixed_value)
                # Parse JSON
                data = ReciveDataSchema.parse_raw(fixed_value)

                # Cập nhật thông tin vào raybot_info
                for key, value in data.dict().items():
                    if value is not None:
                        setattr(self.raybot_info, key, value)
                        if key == "min_distance_move":
                            logger.info(f"Max pwm movement: {value}")

            else:
                # logger.info(f"Recive data: {data}")
                pass
        except Exception as e:
            logger.error(f"Error: {e}")

    def _sanitize_serial_data(self, raw_value: str) -> str:
        """
        Hàm xử lý và sửa lỗi dữ liệu serial trước khi parse thành JSON.
        """
        # Xử lý lỗi 'Expecting property name enclosed in double quotes'
        raw_value = re.sub(
            r"([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r'\1"\2":', raw_value
        )

        # Xử lý lỗi 'Unterminated string' hoặc thiếu dấu nháy kép
        raw_value = re.sub(r":\s*([a-zA-Z0-9_.-]+)", r': "\1"', raw_value)

        # Xử lý giá trị float không hợp lệ (vd: "31v74.7")
        raw_value = re.sub(r"([0-9]+)v([0-9.]+)", r"\1.\2", raw_value)

        # Đảm bảo không có dấu phẩy thừa
        raw_value = raw_value.rstrip(",")  # Xóa dấu phẩy thừa cuối chuỗi

        return raw_value

    def handle_move_forward(self, id, data):
        logger.warning("Move forward")
        if self.raybot_info.lift_distance > self.raybot_info.min_distance_lift:
            self.send_command(CommandEnum.lift_box)
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != CommandEnum.lift_box
                and not self.stop_event.is_set()
            ):
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    return
                if not self.send_command(CommandEnum.lift_box):
                    count_send_error += 1
                sleep(0.01)
            while (
                self.raybot_info.lift_distance > self.raybot_info.min_distance_lift
                and not self.stop_event.is_set()
            ):
                sleep(0.01)
            self.send_command(CommandEnum.stop)
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(CommandEnum.forward)
        while not self.stop_event.is_set():
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != CommandEnum.forward
                and not self.stop_event.is_set()
            ):
                sleep(0.01)

                if self.send_command(CommandEnum.forward):
                    break
                count_send_error += 1
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    break
            logger.info("QR code: " + self.raybot_info.qr_location)
            if data and data.get("location"):
                if self.raybot_info.qr_location == data.get("location"):
                    self.send_command(CommandEnum.stop)
                    # sleep(0.01)
                    command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)
                    break
            else:
                command_manager.update_status(id, CommandStatusEnum.SUCCESS)
                break
            sleep(0.01)
        logger.warning("Stop")

    def handle_move_to_location(self, id, data):
        logger.warning("Move forward")
        direction = data.get("direction").lower()
        if direction not in [
            CommandEnum.forward,
            CommandEnum.backward,
        ]:
            command_manager.update_status(
                id,
                CommandStatusEnum.FAILED,
                {"reason": "Command data is invalid: direction is invalid"},
            )
            return
        location = data.get("location")
        if not location:
            command_manager.update_status(
                id,
                CommandStatusEnum.FAILED,
                {"reason": "Command data is invalid: location is required"},
            )
            return
        # open here went to production
        if self.raybot_info.lift_distance > self.raybot_info.min_distance_lift:
            self.send_command(CommandEnum.lift_box)
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != CommandEnum.lift_box
                and not self.stop_event.is_set()
            ):
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    return
                if not self.send_command(CommandEnum.lift_box):
                    count_send_error += 1
                sleep(0.01)
            while (
                self.raybot_info.lift_distance > self.raybot_info.min_distance_lift
                and not self.stop_event.is_set()
            ):
                sleep(0.01)
            self.send_command(CommandEnum.stop)
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(direction)
        while not self.stop_event.is_set():
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != direction
                and not self.stop_event.is_set()
            ):
                sleep(0.01)

                if self.send_command(direction):
                    break
                count_send_error += 1
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    break
            before = self.raybot_info.qr_location
            if before != self.raybot_info.qr_location:
                logger.info("QR code: " + self.raybot_info.qr_location)
            if data:
                if self.raybot_info.qr_location == data.get("location"):
                    self.send_command(CommandEnum.stop)
                    # sleep(0.01)
                    command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)
                    break
            else:
                command_manager.update_status(id, CommandStatusEnum.SUCCESS)
                break
            sleep(0.01)
        logger.warning("Stop")

    def handle_move_backward(self, id, data):
        logger.warning("Move backward")
        if self.raybot_info.lift_distance > self.raybot_info.min_distance_lift:
            self.send_command(CommandEnum.lift_box)
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != CommandEnum.lift_box
                and not self.stop_event.is_set()
            ):
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    return
                if not self.send_command(CommandEnum.lift_box):
                    count_send_error += 1
                sleep(0.01)
            while (
                self.raybot_info.lift_distance > self.raybot_info.min_distance_lift
                and not self.stop_event.is_set()
            ):
                sleep(0.01)
            self.send_command(CommandEnum.stop)
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(CommandEnum.backward)
        while not self.stop_event.is_set():
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != CommandEnum.backward
                and not self.stop_event.is_set()
            ):
                sleep(0.01)

                if self.send_command(CommandEnum.backward):
                    break
                count_send_error += 1
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    break
            logger.info("QR code: " + self.raybot_info.qr_location)
            if data and data.get("location"):
                if self.raybot_info.qr_location == data.get("location"):
                    self.send_command(CommandEnum.stop)
                    # sleep(0.01)
                    command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)
                    break
            else:
                command_manager.update_status(id, CommandStatusEnum.SUCCESS)
                break
            sleep(0.01)
        logger.warning("Stop")

    def update_config_arduino(self):
        self.send_data(self.raybot_info.dict())

    def handle_drop_box(self, id, data):
        while (
            not self.send_command(CommandEnum.stop)
            and self.raybot_info.current_cmd != CommandEnum.stop
            and not self.stop_event.is_set()
        ):
            sleep(0.01)

        logger.warning("Move drop_item")
        distance = None
        if data:
            distance = data.get("distance")
        if not distance:
            distance = self.raybot_info.max_distance_lift
        else:
            if distance > self.raybot_info.max_distance_lift:
                distance = self.raybot_info.max_distance_lift
        logger.info(f"Drop box at distance: {distance}")
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(CommandEnum.drop_box)
        while not self.stop_event.is_set():
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != CommandEnum.drop_box
                and not self.stop_event.is_set()
            ):
                sleep(0.01)

                if self.send_command(CommandEnum.drop_box):
                    break
                count_send_error += 1
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    return
            # logger.info(f"Drop distance: {self.raybot_info.lift_distance}")
            if self.raybot_info.lift_distance > distance:
                self.send_command(CommandEnum.stop)
                # sleep(0.01)
                command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)
                break
            sleep(0.01)
            # comment here went to production
            # break
        command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)
        logger.warning("Stop")

    def handle_lift_box(self, id, data):
        while (
            not self.send_command(CommandEnum.stop)
            and self.raybot_info.current_cmd != CommandEnum.stop
            and not self.stop_event.is_set()
        ):
            sleep(0.1)
        logger.warning("Move pick_item")
        distance = None
        if data:
            distance = data.get("distance")
        if distance:
            if distance < self.raybot_info.min_distance_lift:
                distance = self.raybot_info.min_distance_lift
        else:
            distance = self.raybot_info.min_distance_lift
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(CommandEnum.lift_box)
        while not self.stop_event.is_set():
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != CommandEnum.lift_box
                and not self.stop_event.is_set()
            ):
                sleep(0.01)

                if self.send_command(CommandEnum.lift_box):
                    command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)
                    break
                count_send_error += 1
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    break

            if self.raybot_info.lift_distance < distance:
                self.send_command(CommandEnum.stop)
                # sleep(0.01)
                command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)
                break
            sleep(0.01)
            # comment here went to production
            # break
        command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)
        logger.warning("Stop")

    def handle_open_box(self, id, data):
        while (
            not self.send_command(CommandEnum.stop)
            and self.raybot_info.current_cmd != CommandEnum.stop
            and not self.stop_event.is_set()
        ):
            sleep(0.1)
        logger.warning("Open box")
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(CommandEnum.open_box)
        count_send_error = 0
        while (
            self.raybot_info.current_cmd != CommandEnum.open_box
            and not self.stop_event.is_set()
        ):
            if not self.send_command(CommandEnum.open_box):
                count_send_error += 1
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    return
            sleep(0.01)

        # while self.raybot_info.door_state != 1 and not self.stop_event.is_set():
        #     sleep(0.01)
        command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)

    def handle_close_box(self, id, data):
        while (
            not self.send_command(CommandEnum.stop)
            and self.raybot_info.current_cmd != CommandEnum.stop
            and not self.stop_event.is_set()
        ):
            sleep(0.1)
        logger.warning("Close box")
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(CommandEnum.close_box)
        count_send_error = 0
        while (
            self.raybot_info.current_cmd != CommandEnum.close_box
            and not self.stop_event.is_set()
        ):
            if not self.send_command(CommandEnum.close_box):
                count_send_error += 1
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    return
            sleep(0.01)

        # while self.raybot_info.door_state != 0:
        #     sleep(0.01)
        command_manager.update_status(id, CommandStatusEnum.SUCCESS)

    def handle_check_qr(self, id, data):
        self.raybot_info.qr_door = ""
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(CommandEnum.stop)
        logger.warning("Scan QR code")
        qr_code = None
        if data:
            qr_code = data.get("qr_code")
        logger.info(f"QR code: {qr_code}")
        logger.info(f"QR code: {self.raybot_info.qr_door}")
        # sleep(5)
        # command_manager.update_status(
        #     id, CommandStatusEnum.SUCCESS, {"qr_code": qr_code}
        # )
        if qr_code:
            while not self.stop_event.is_set():
                logger.info(f"QR code: {qr_code}")
                logger.info(f"QR code: {self.raybot_info.qr_door}")
                if self.raybot_info.qr_door == qr_code:
                    command_manager.update_status(id, CommandStatusEnum.SUCCESS, data)
                    self.raybot_info.qr_door = ""
                    break
                sleep(0.01)
        else:
            command_manager.update_status(
                id, CommandStatusEnum.FAILED, {"reason": "Command data is invalid"}
            )
        logger.warning("QR code found")

    def handle_speak(self, id, data):
        logger.warning("Speak text")
        text = None
        if data:
            text = data.get("text")
        if not text:
            command_manager.update_status(
                id, CommandStatusEnum.FAILED, {"reason": "Command data is invalid"}
            )
            return
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        speak(text)
        command_manager.update_status(id, CommandStatusEnum.SUCCESS)
        logger.warning("Speak text")

    def handle_scan_location(self, id, data):
        if self.raybot_info.lift_distance > self.raybot_info.min_distance_lift:
            self.send_command(CommandEnum.lift_box)
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != CommandEnum.lift_box
                and not self.stop_event.is_set()
            ):
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    return
                if not self.send_command(CommandEnum.lift_box):
                    count_send_error += 1
                sleep(0.01)
            while (
                self.raybot_info.lift_distance > self.raybot_info.min_distance_lift
                and not self.stop_event.is_set()
            ):
                sleep(0.01)
            self.send_command(CommandEnum.stop)
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(CommandEnum.forward)
        qr_codes = []
        while not self.stop_event.is_set():
            count_send_error = 0
            while (
                self.raybot_info.current_cmd != CommandEnum.forward
                and not self.stop_event.is_set()
            ):
                sleep(0.01)

                if self.send_command(CommandEnum.forward):
                    break
                count_send_error += 1
                if count_send_error > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    self.send_command(CommandEnum.stop)
                    break
            logger.info("QR code: " + self.raybot_info.qr_location)
            if self.raybot_info.qr_location != "":
                if len(qr_codes) == 0:
                    qr_codes.append(self.raybot_info.qr_location)
                elif qr_codes[-1] != self.raybot_info.qr_location:
                    qr_codes.append(self.raybot_info.qr_location)
                if self.raybot_info.qr_location == qr_codes[0] and len(qr_codes) > 1:
                    self.send_command(CommandEnum.stop)
                    command_manager.update_status(
                        id, CommandStatusEnum.SUCCESS, {"qr_codes": qr_codes}
                    )
                    break

            sleep(0.01)
        logger.warning("Stop")

    def handle_stop(self, id, data):
        logger.warning("Stop")
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        self.send_command(CommandEnum.stop)
        count = 0
        while (
            self.raybot_info.current_cmd != CommandEnum.stop
            and not self.stop_event.is_set()
        ):
            sleep(0.01)
            # logger.info(self.raybot_info.current_cmd)
            if not self.send_command(CommandEnum.stop):
                count += 1
                if count > 3:
                    command_manager.update_status(
                        id, CommandStatusEnum.FAILED, {"reason": "Send command error"}
                    )
                    return
        command_manager.update_status(id, CommandStatusEnum.SUCCESS)
        logger.warning("Stop")

    def handle_wait_get_item(self, id, data):
        logger.warning("Wait get item")
        command_manager.update_status(id, CommandStatusEnum.IN_PROGRESS)
        sleep(10)
        command_manager.update_status(id, CommandStatusEnum.SUCCESS)
        while self.raybot_info.weight != 0 and not self.stop_event.is_set():
            sleep(0.01)
            if self.raybot_info.weight == 0:
                command_manager.update_status(id, CommandStatusEnum.SUCCESS)

    def execute_command(self, msg: CommandReciveSchema):
        if not msg:
            logger.error("Command is empty")
            return
        msg.type = msg.type.lower()
        # if msg.type not in self.commands:
        #     logger.error(f"Command {msg.type} is not implemented.")
        #     command_manager.update_status(
        #         msg.id,
        #         CommandStatusEnum.FAILED,
        #         {"reason": "Command is not implemented"},
        #     )
        #     return

        with self.lock:  # Đảm bảo rằng chỉ có một lệnh được thực thi tại một thời điểm
            # Nếu có thread đang chạy, dừng nó
            if self.command_thread and self.command_thread.is_alive():
                logger.info("Stop current command thread")
                self.stop_event.set()
                # self.command_thread.stop()
                self.command_thread.join()

            # Reset event để lệnh mới không bị dừng ngay lập tức
            self.stop_event.clear()

            # Lấy tên hàm từ enum và gọi hàm đó
            method_name = msg.type
            logger.info(f"Execute command: {method_name}")
            method = getattr(self, f"handle_{method_name}", None)

            if method:
                # Tạo thread mới để thực thi lệnh
                self.command_thread = threading.Thread(
                    target=method, args=(msg.id, msg.data), daemon=True
                )
                self.command_thread.start()
            else:
                logger.error(f"Command {method_name} is not implemented.")

    def run(self):
        logger.info("Raybot service started")
        default = {
            "max_pwm_movement": self.raybot_info.max_pwm_movement,
            "max_pwm_lift": self.raybot_info.max_pwm_lift,
            "home_location": self.raybot_info.home_location,
            "max_distance_lift": self.raybot_info.max_distance_lift,
            "min_distance_move": self.raybot_info.min_distance_move,
            "min_distance_lift": self.raybot_info.min_distance_lift,
        }
        self.send_data(default)
        while True:
            try:
                if self.serial.in_waiting > 0:
                    data = self.serial.readline().decode("utf-8").strip()
                    # logger.info(f"Received: {data}")
                    self._handle_recive_data(data)
                sleep(0.001)
            except Exception as e:
                logger.info(f"Error: {e}")

    def close(self):
        try:
            self.serial.close()
            logger.info("Closed")
        except Exception as e:
            logger.info(f"Error: {e}")

    def start(self):
        logger.info("Raybot service started")
        Thread.start(self)


raybot = RaybotService(
    serial_config=SerialSchemas(**config_service.get_config(section="serial")),
    raybot_config=RaybotConfigSchema(**config_service.get_config(section="raybot")),
)

# raybot.send_command(CommandEnum.forward, DataCommandEnum.pwm)
