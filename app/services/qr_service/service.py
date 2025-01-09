import random
import threading
import time
from threading import Thread
from app.config import qr_serial_config, cam_serial_config

from app.services.qr_service.camera.cameraQR.cameraQR import camera_manager
import serial

from app.services.raybot.service import raybot

# Biến chia sẻ
qr_code_lock = threading.Lock()


class Listener:
    def update(self, data):
        # print(f"[Listener] Đã nhận dữ liệu mới: {data}")
        pass


listeners: dict[str, Listener] = {}


# Worker thread để đọc mã QR từ UART (giả lập)
def read_qr_code():
    global qr_code_data
    count = 0
    qr_codes = [
        "table_1",
        "table_2",
        "table_3",
        "table_4",
        "table_5",
        "table_6",
        "table_7",
        "table_8",
        "table_9",
        "table_10",
        "table_11",
        "table_12",
    ]
    while True:
        # Giả lập việc đọc mã QR từ UART
        fake_qr_code = qr_codes[count]
        count += 1
        if count >= len(qr_codes):
            count = 0
        # Cập nhật biến chia sẻ với write lock
        with qr_code_lock:
            qr_code_data = fake_qr_code
            for listener in listeners.values():
                listener.update(fake_qr_code)

            # raybot.raybot_info.qr_door = fake_qr_code
            # raybot.raybot_info.qr_location = fake_qr_code
        # print(f"[UART Worker] Đã đọc mã QR: {fake_qr_code}")
        time.sleep(1)  # Giả lập thời gian đọc mã QR


def get_qr_code():
    # uart = serial.Serial(
    #     cam_serial_config.port,
    #     cam_serial_config.baudrate,
    #     timeout=cam_serial_config.timeout,
    # )
    # app.active(mode="camQrLocation", read_qr=True)
    print("Start get qr code")
    while True:
        # if uart.in_waiting:
        #     try:
        #         qr_code = uart.read(uart.in_waiting).decode("utf-8").strip()
        #         if qr_code:
        #             print(f"[UART Worker] Đã đọc mã QR: {qr_code}")
        #             # with qr_code_lock:
        #             #     raybot.raybot_info.qr_location = qr_code
        #     except Exception as e:
        #         print(e)
        if camera_manager.qr_flag:
            print(camera_manager.status["camQrLocation"]["last_qr"])
            with qr_code_lock:
                raybot.raybot_info.qr_location = camera_manager.status["camQrLocation"][
                    "last_qr"
                ]
            camera_manager.qr_flag = False
        if camera_manager.qr_box_flag:
            print(camera_manager.status["camQrCheckBox"]["last_qr"])
            with qr_code_lock:
                raybot.raybot_info.qr_door = camera_manager.status["camQrCheckBox"][
                    "last_qr"
                ]
            camera_manager.qr_box_flag = False
        time.sleep(0.01)  # Giảm tải CPU


listener = Listener()
listeners["qr_listener"] = listener
listeners["qr_listener2"] = listener


# Khởi tạo và chạy các thread
# qr_thread = threading.Thread(target=read_qr_code, daemon=True)

qr_thread2 = threading.Thread(target=get_qr_code, daemon=True)
# qr_thread.start()
