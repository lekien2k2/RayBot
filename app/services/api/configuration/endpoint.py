import logging
from fastapi import APIRouter, Query, Response, status
from app.services.raybot.service import raybot
from app.config import config_service
from app.services.api.configuration.schema import (
    ConfigResponeSchema,
    UpdateConfigSchema,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=ConfigResponeSchema)
def get_config():
    config = config_service.load_config()
    return config["raybot"]


@router.put("/raybot")
def update_raybot_config(config: UpdateConfigSchema):
    for key, value in config.dict().items():
        if value is not None:
            config_service.update_config(section="raybot", key=key, value=value)
            raybot.send_data({key: value})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/serial")
def update_serial_config(config: UpdateConfigSchema):
    config_service.update_config(section="serial", key=config.key, value=config.value)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/qr_serial")
def update_qr_serial_config(config: UpdateConfigSchema):
    config_service.update_config(
        section="qr_serial", key=config.key, value=config.value
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/cam_serial")
def update_cam_serial_config(config: UpdateConfigSchema):
    config_service.update_config(
        section="cam_serial", key=config.key, value=config.value
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/server")
def update_server_config(config: UpdateConfigSchema):
    config_service.update_config(section="server", key=config.key, value=config.value)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
