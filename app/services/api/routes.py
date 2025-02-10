from fastapi import APIRouter

# from app.services.api.audit_logs.endpoint import router as audit_logs_router
# from app.services.api.auth.dependencies import RequiredAuth
# from app.services.api.auth.endpoint import router as auth_router

# from app.services.api.configuration.endpoint import router as configuration_router
# from app.services.api.data.endpoint import router as data_router
# from app.services.api.device.endpoint import router as device_router
# from app.services.api.device_template.endpoint import router as device_template_router
from app.services.api.logs.endpoint import router as log_router
from app.services.api.command.endpoint import router as command_router

# from app.services.api.system.endpoint import router as system_router
# from app.services.api.user.endpoint import router as user_router
# from app.services.api.warning_data_logs.endpoint import (
#     router as warning_data_logs_router,
# )
from app.services.api.firmware.endpoint import router as firmware_router
from app.services.api.configuration.endpoint import router as config_router
from app.services.api.camera.endpoint import router as camera_router

router = APIRouter()

# router.include_router(auth_router, prefix="/auth", tags=["auth"])
# router.include_router(
#     user_router, prefix="/users", tags=["users"], dependencies=[RequiredAuth]
# )
# router.include_router(
#     device_router, prefix="/devices", tags=["devices"], dependencies=[RequiredAuth]
# )
# router.include_router(
#     system_router, prefix="/system", tags=["system"], dependencies=[RequiredAuth]
# )
# router.include_router(
#     data_router, prefix="/data", tags=["data"], dependencies=[RequiredAuth]
# )
# router.include_router(
#     device_template_router,
#     prefix="/device_templates",
#     tags=["device_templates"],
#     dependencies=[RequiredAuth],
# )
router.include_router(log_router, prefix="/logs", tags=["logs"])
# router.include_router(
#     configuration_router,
#     prefix="/configuration",
#     tags=["configuration"],
#     dependencies=[RequiredAuth],
# )

# router.include_router(
#     audit_logs_router,
#     prefix="/audit_logs",
#     tags=["audit_logs"],
#     dependencies=[RequiredAuth],
# )

# router.include_router(
#     warning_data_logs_router,
#     prefix="/warning_data_logs",
#     tags=["warning_data_logs"],
#     dependencies=[RequiredAuth],
# )

router.include_router(
    firmware_router,
    prefix="/firmware",
    tags=["firmware"],
)

router.include_router(
    config_router,
    prefix="/config",
    tags=["config"],
)

router.include_router(
    camera_router,
    prefix="/camera",
    tags=["camera"],
)

router.include_router(
    command_router,
    prefix="/command",
    tags=["command"],
)
