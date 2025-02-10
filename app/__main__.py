# import logging
# from time import sleep

# from app.services.logging import init_logger
# from app.constants import LOG_LEVEL

# init_logger(LOG_LEVEL, enable_db_hanlder=False)
# logger = logging.getLogger(__name__)
# from app.config import server_config

# # from app.services.qr_service.service import qr_code_data
# from app.services.raybot.service import raybot
# from app.services.websockets.service2 import WebSocketClient, WebSocketServer
# from app.test import func
# from app.services.api.service import APIService
# from app.database.func import check_db
# from app.services.qr_service.service import qr_thread2


# def main():
#     logger.info("Starting main")
#     check_db()
#     api = APIService()
#     client = WebSocketClient(
#         server_config.protocol,
#         server_config.host,
#         server_config.port,
#         server_config.path,
#         server_config.timeout,
#         server_config.id,
#     )
#     server = WebSocketServer("0.0.0.0", 8765)
#     raybot.start()
#     server.start()
#     # client.start()
#     qr_thread2.start()
#     # server.send("GET", "test", "1", {"data": "test"})
#     # raybot.send_command("forward1", "pwm")
#     # server.run()
#     # while True:
#     #     sleep(1000)
#     api.start()
#     # app.run()


# if __name__ == "__main__":
#     main()

import logging
from time import sleep

from app.services.logging import init_logger
from app.constants import LOG_LEVEL

init_logger(LOG_LEVEL, enable_db_hanlder=False)
logger = logging.getLogger(__name__)
from app.config import server_config

# from app.services.qr_service.service import qr_code_data
from app.services.raybot.service import raybot
from app.services.websockets.service import AsyncWebSocketClient, WebSocketServer
from app.test import func
from app.services.api.service import APIService
from app.database.func import check_db
from app.services.qr_service.service import qr_thread2
import asyncio


async def main_async():
    """Chạy WebSocket client + Chạy API, raybot, QR scanner trong thread"""
    logger.info("Starting main (async)")

    # Khởi tạo WebSocket Client
    client = AsyncWebSocketClient(
        server_config.protocol,
        server_config.host,
        server_config.port,
        server_config.path,
        server_config.timeout,
        server_config.id,
    )
    server = WebSocketServer("0.0.0.0", 8765)
    # Chạy API, Raybot, QR Scanner trong thread
    api = APIService()

    # Chạy các service trong thread (tránh block asyncio)
    loop = asyncio.get_running_loop()
    api_thread = loop.run_in_executor(None, api.start)
    raybot_thread = loop.run_in_executor(None, raybot.start)
    qr_thread = loop.run_in_executor(None, qr_thread2.start)
    server_thread = loop.run_in_executor(None, server.start)
    # Chờ WebSocket hoàn tất
    await client.run()

    # Chờ các thread hoàn thành (chúng chạy vô hạn, không kết thúc)
    await asyncio.gather(api_thread, raybot_thread, qr_thread, server_thread)


if __name__ == "__main__":
    asyncio.run(main_async())
