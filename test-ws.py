import argparse
import logging
import time
from datetime import datetime
from typing import Any, Optional

from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("websocket_client.log"), logging.StreamHandler()],
)

# Constants
MAX_RECONNECT_ATTEMPTS = 5  # Maximum number of reconnection attempts
RECONNECT_DELAY = 5  # Delay between reconnection attempts in seconds
# WS_URL = "ws://localhost:8080/ws-raybot"
WS_URL = "ws://192.168.1.173:8082/robots/ws-raybot"


class WebSocketClient:
    def __init__(self, client_id: str) -> None:
        self.client_id = client_id
        self.reconnect_count = 0
        self.connection_history: list[dict[str, Any]] = []
        self.current_connection_start: Optional[float] = None
        self.is_running = True

    def connect_to_server(self) -> bool:
        """Attempt to connect to the WebSocket server"""
        uri = f"{WS_URL}?id={self.client_id}"
        try:
            self.websocket = connect(uri)
            self.current_connection_start = time.time()
            logging.info(f"Connected to server at {WS_URL} with id {self.client_id}")
            return True
        except Exception as e:
            logging.error(f"Failed to connect: {e}")
            return False

    def record_connection_time(self) -> None:
        """Record the duration of the current connection"""
        if self.current_connection_start:
            duration = time.time() - self.current_connection_start
            self.connection_history.append(
                {
                    "start_time": datetime.fromtimestamp(self.current_connection_start),
                    "duration": duration,
                }
            )
            logging.info(f"Connection session lasted: {duration:.2f} seconds")

    def run(self) -> None:
        """Main execution loop with auto-reconnect"""
        while self.is_running:
            try:
                if not self.connect_to_server():
                    raise ConnectionError("Failed to connect to server")

                # Main message receiving loop
                while True:
                    try:
                        _ = self.websocket.recv()
                    except TimeoutError:
                        logging.warning("Timeout: No response from server")
                    except ConnectionClosed:
                        raise  # Re-raise to trigger reconnection

            except (ConnectionClosed, ConnectionError, OSError):
                self.record_connection_time()
                self.reconnect_count += 1

                if self.reconnect_count >= MAX_RECONNECT_ATTEMPTS:
                    logging.error(
                        f"Max reconnection attempts ({MAX_RECONNECT_ATTEMPTS}) reached. Shutting down."
                    )
                    break

                logging.warning(
                    f"Connection lost. Reconnection attempt {self.reconnect_count}/{MAX_RECONNECT_ATTEMPTS} in {RECONNECT_DELAY} seconds..."
                )
                time.sleep(RECONNECT_DELAY)

            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                break

    def shutdown(self) -> None:
        """Gracefully shutdown the client"""
        self.is_running = False
        self.record_connection_time()

        # Print connection statistics
        total_duration = sum(session["duration"] for session in self.connection_history)
        logging.info("Connection Statistics:")
        logging.info(f"Total reconnection attempts: {self.reconnect_count}")
        logging.info(f"Total connection time: {total_duration:.2f} seconds")
        logging.info("Connection History:")
        for i, session in enumerate(self.connection_history, 1):
            logging.info(f"Session {i}:")
            logging.info(f"  Start time: {session['start_time']}")
            logging.info(f"  Duration: {session['duration']:.2f} seconds")

        if hasattr(self, "websocket"):
            self.websocket.close()
        logging.info("Client shutdown complete")


def main() -> None:
    parser = argparse.ArgumentParser(description="WebSocket Client with Auto-reconnect")
    parser.add_argument(
        "--id",
        type=str,
        required=True,
        help="The unique ID to connect to the WebSocket server",
    )
    args = parser.parse_args()

    client = WebSocketClient(args.id)
    try:
        client.run()
    except KeyboardInterrupt:
        logging.info("\nShutdown requested by user...")
    finally:
        client.shutdown()


if __name__ == "__main__":
    main()


# Mai test thì lấy code này nha
