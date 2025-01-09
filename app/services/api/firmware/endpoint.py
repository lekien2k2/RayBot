import os
import shutil
from typing import Literal, Optional
import uuid
import zipfile
import subprocess
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Form,
    HTTPException,
    Request,
    File,
    UploadFile,
)
from fastapi.responses import JSONResponse
from orjson import orjson

UPLOAD_FOLDER = "/tmp/arduino_firmware"
ALLOWED_EXTENSIONS = {".zip"}

router = APIRouter()


def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


def extract_firmware(uploaded_file):
    # Tạo thư mục tạm
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Giải nén file
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        zip_ref.extractall(UPLOAD_FOLDER)

    return UPLOAD_FOLDER


def build_firmware(sketch_path):
    try:
        # Biên dịch firmware
        compile_cmd = [
            "arduino-cli",
            "compile",
            "--fqbn",
            "arduino:avr:uno",  # Điều chỉnh board phù hợp
            sketch_path,
        ]
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)

        if compile_result.returncode != 0:
            return False, compile_result.stderr

        return True, "Compilation successful"

    except Exception as e:
        return False, str(e)


# Xử lý upload firmware
def process_firmware_upload(
    file_path: str,
    board_type: str,
    board_model: Optional[str] = None,
    port: Optional[str] = "/dev/ttyACM0",
):
    try:
        # Giải nén file
        extract_path = os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()))
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        # Xác định phương thức build dựa trên loại board
        if board_type == "platformio":
            # Kiểm tra cấu trúc PlatformIO
            if not os.path.exists(os.path.join(extract_path, "platformio.ini")):
                raise ValueError("Invalid PlatformIO project structure")

            # Build và upload sử dụng PlatformIO
            build_cmd = ["pio", "run", "-d", extract_path]
            upload_cmd = [
                "pio",
                "run",
                "-t",
                "upload",
                "-d",
                extract_path,
                "--upload-port",
                port or "/dev/ttyACM0",
            ]

        elif board_type == "arduino":
            # Kiểm tra file .ino
            ino_files = [f for f in os.listdir(extract_path) if f.endswith(".ino")]
            if not ino_files:
                raise ValueError("No Arduino sketch found")

            # Build và upload sử dụng Arduino CLI
            build_cmd = [
                "arduino-cli",
                "compile",
                "--fqbn",
                board_model or "arduino:avr:uno",
                extract_path,
            ]
            upload_cmd = [
                "arduino-cli",
                "upload",
                "--fqbn",
                board_model or "arduino:avr:uno",
                "-p",
                port or "/dev/ttyACM0",
                extract_path,
            ]

        else:
            raise ValueError("Unsupported board type")

        # Thực thi build
        build_result = subprocess.run(build_cmd, capture_output=True, text=True)
        if build_result.returncode != 0:
            raise subprocess.CalledProcessError(
                build_result.returncode, build_cmd, build_result.stderr
            )

        # Thực thi upload
        upload_result = subprocess.run(upload_cmd, capture_output=True, text=True)
        if upload_result.returncode != 0:
            raise subprocess.CalledProcessError(
                upload_result.returncode, upload_cmd, upload_result.stderr
            )

        return "Upload successful"

    except Exception as e:
        raise ValueError(f"Firmware upload failed: {str(e)}")
    finally:
        # Dọn dẹp file tạm
        shutil.rmtree(extract_path, ignore_errors=True)


@router.post("/upload-firmware")
async def upload_firmware(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    board_type: Literal["arduino", "platformio"] = Form(...),
    board_model: Optional[str] = Form(None),
    port: Optional[str] = Form("/dev/ttyACM0"),
):
    # Khởi tạo ID upload
    upload_id = str(uuid.uuid4())

    # Lưu file tạm
    file_path = os.path.join(UPLOAD_FOLDER, f"{upload_id}_{file.filename}")

    # Tạo thư mục upload nếu chưa tồn tại
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Lưu file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Chuẩn bị thông tin upload
    # upload_info = FirmwareUpload(
    #     id=upload_id,
    #     filename=file.filename,
    #     board_type=board_type,
    #     status="pending",
    #     board_model=board_model,
    #     port=port,
    # )

    # # Ghi log upload
    # log_upload(upload_info)

    try:
        # Xử lý upload trong background
        background_tasks.add_task(
            process_firmware_upload, file_path, board_type, board_model, port
        )

        return {"message": "Firmware upload started", "upload_id": upload_id}

    except Exception as e:
        # Cập nhật trạng thái lỗi
        # update_upload_status(upload_id, "failed")

        # Xóa file tạm
        os.remove(file_path)

        raise HTTPException(status_code=400, detail=str(e))
