import time

import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import threading
import os


class Config:
    DEFAULT_CONFIG = {
        "camQrLocation": 0,
        "camQrCheckBox": 1,
        "portStreamLocation": 9999,
        "resolution": (320, 320),
    }

    def __init__(
        self, config_file="./app/services/qr_service/camera/cameraQR/config.txt"
    ):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            self.save_config(Config.DEFAULT_CONFIG)
            print("DEFAULT")

        with open(self.config_file, "r") as file:
            lines = file.readlines()
            print(lines)
            self.config = {
                key.strip(): self._parse_value(value.strip())
                for key, value in (line.split("=") for line in lines)
            }

    def save_config(self, config):
        with open(self.config_file, "w") as file:
            for key, value in config.items():
                file.write(f"{key} = {value}\n")

    @staticmethod
    def _parse_value(value):
        try:
            if "," in value:
                return tuple(map(int, value.strip("() ").split(",")))
            return int(value)
        except ValueError:
            return value

    def update_config(self, **kwargs):
        self.config.update(kwargs)
        self.save_config(self.config)


class CameraManager:
    def __init__(self, config):
        self.config = config
        self.status = {
            "camQrLocation": {"state": "stop", "last_qr": None},
            "camQrCheckBox": {"state": "stop", "last_qr": None},
        }
        self.qr_data = {"camQrLocation": None, "camQrCheckBox": None}
        self.qr_flag = False
        self.qr_box_flag = False
        self.frames = {}  # Store frames for each mode
        self.camera_threads = {}  # Keep track of camera threads

    def start_camera(self, camera_id, mode):
        camera = cv2.VideoCapture(camera_id)
        self.status[mode]["state"] = "running"
        time_check = time.time()
        while True:
            success, frame = camera.read()
            if not success:
                time.sleep(0.1)
                print(camera_id, mode, "is not running")
                continue

            # Resize and save the frame
            frame = cv2.resize(frame, self.config["resolution"])
            self.frames[mode] = frame

            # QR Code decoding logic
            decoded_objects = decode(frame, symbols=[ZBarSymbol.QRCODE])
            for obj in decoded_objects:
                qr_text = obj.data.decode("utf-8")
                if mode == "camQrLocation" and qr_text != self.status[mode]["last_qr"]:
                    self.status[mode]["last_qr"] = qr_text
                    print(f"New QR code detected: {qr_text}")
                    self.qr_data[mode] = qr_text
                    self.qr_flag = True

                elif (
                    mode == "camQrCheckBox"
                    and time.time() - time_check > 2
                    or qr_text != self.status[mode]["last_qr"]
                ):
                    time_check = time.time()
                    self.qr_box_flag = True
                    self.status[mode]["last_qr"] = qr_text
                    print(f"New QR code detected: {qr_text}")
                    self.qr_data[mode] = qr_text
        camera.release()

    def generate_video_stream(self, mode):
        while True:
            frame = self.frames.get(mode)
            if frame is None:
                time.sleep(0.1)
                continue

            _, buffer = cv2.imencode(".jpg", frame)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )

    def start_background_camera(self, mode):
        camera_id = self.config.get(mode)
        if not camera_id and camera_id != 0:
            return

        if mode not in self.camera_threads:
            thread = threading.Thread(
                target=self.start_camera, args=(camera_id, mode), daemon=True
            )
            self.camera_threads[mode] = thread
            thread.start()


config = Config().config

camera_manager = CameraManager(config)

camera_manager.start_background_camera("camQrLocation")
camera_manager.start_background_camera("camQrCheckBox")


# class QRApp:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.setup_routes()

#     def setup_routes(self):
#         @self.app.route("/get_last_qr", methods=["GET"])
#         def get_last_qr():
#             mode = request.args.get("mode", "camQrLocation")
#             return {"last_qr": camera_manager.qr_data.get(mode)}

#         @self.app.route("/video_feed", methods=["GET"])
#         def video_feed():
#             mode = request.args.get("mode", "camQrLocation")
#             camera_id = config.get(mode)
#             if not camera_id and camera_id != 0:
#                 return "Invalid camera mode", 400

#             return Response(
#                 camera_manager.generate_video_stream(mode),
#                 mimetype="multipart/x-mixed-replace; boundary=frame",
#             )

#     def run(self):
#         # self.camera_manager.start_background_camera("camQrLocation")
#         # self.camera_manager.start_background_stream("camQrCheckBox")
#         self.app.run(
#             host="0.0.0.0", port=self.config["portStreamLocation"], debug=False
#         )

#     # if __name__ == "__main__":


# app = QRApp()
