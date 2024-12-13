import logging
from time import sleep

from app.config import server_config
from app.services.logging import init_logger
from app.services.qr_service.service import qr_code_data
from app.services.raybot.service import raybot
from app.services.websockets.service import WebSocketClient, WebSocketServer
from app.test import func
from app.constants import LOG_LEVEL

init_logger(LOG_LEVEL, enable_db_hanlder=False)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting main")
    func()
    client = WebSocketClient(
        server_config.protocol,
        server_config.host,
        server_config.port,
        server_config.path,
        server_config.timeout,
        server_config.id,
    )
    server = WebSocketServer("0.0.0.0", 8765)
    raybot.start()
    server.start()
    client.start()
    # server.send("GET", "test", "1", {"data": "test"})
    # raybot.send_command("forward1", "pwm")
    # server.run()
    while True:
        sleep(1000)


if __name__ == "__main__":
    main()
