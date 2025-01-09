from threading import Thread

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import config_service
from app.services.api.config import fastapi_config
from app.services.api.routes import router
from app.services.base import BaseService


class APIService(BaseService, Thread):
    def __init__(self):
        BaseService.__init__(self)
        Thread.__init__(self)
        self.daemon = True

        self.app = FastAPI(
            **fastapi_config,
            default_response_class=ORJSONResponse,
        )

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # self.app.add_middleware(AuditLogMiddleware)

        self.app.include_router(router, prefix="/api")
        # Serve the frontend
        # self.app.mount(
        #     "/assets", StaticFiles(directory="app/dist/assets"), name="assets"
        # )

        # @self.app.get("/{catchall:path}")
        # def serve_frontend(catchall: str):
        #     return FileResponse("app/dist/index.html")

    def run(self) -> None:
        uvicorn.run(
            self.app,
            host=config_service.get_config(section="raybot", key="API_HOST"),
            port=config_service.get_config(section="raybot", key="API_PORT"),
            log_config=None,
            # ssl_keyfile="app/self-signed.key",
            # ssl_certfile="app/self-signed.crt",
        )

    def stop(self) -> None:
        pass

    def start(self) -> None:
        self.run()
