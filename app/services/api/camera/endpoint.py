import logging
from fastapi import APIRouter, Query, Response, status
from fastapi.responses import StreamingResponse

from app.services.qr_service.camera.cameraQR.cameraQR import camera_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/video_feed", status_code=status.HTTP_200_OK)
async def video_feed(mode: str = Query("camQrLocation")):
    if mode not in camera_manager.config:
        return "Invalid camera mode", 400
    return StreamingResponse(
        camera_manager.generate_video_stream(mode),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.get("/get_last_qr", status_code=status.HTTP_200_OK)
async def get_last_qr(mode: str = Query("camQrLocation")):
    if mode not in camera_manager.config:
        return "Invalid camera mode", 400
    return {"last_qr": camera_manager.qr_data.get(mode)}


@router.get("/get_qr_flag", status_code=status.HTTP_200_OK)
async def get_qr_flag():
    return {"qr_flag": camera_manager.qr_flag}
