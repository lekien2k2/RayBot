import json
import logging
import threading
import time
from queue import Queue
from threading import Lock, Thread
from time import sleep

from enum import Enum
from typing import Any, Dict, Set
import uuid

import websockets

from websockets.exceptions import ConnectionClosed, WebSocketException
from websockets.sync.client import connect
from websockets.sync.server import serve

from app.services.commands.service import command_manager
from app.services.raybot.service import raybot
from app.services.websockets.schemas import (
    BackwardDistanceSensorMsgType,
    BatteryMsgType,
    CommandReciveSchema,
    DoorStateMsgType,
    ForwardDistanceSensorMsgType,
    LiftDistanceSensorMsgType,
    LiftMotorMsgType,
    MovementMotorMsgType,
    OperationEnum,
    SafetyMsgType,
    SendSchema,
    TopicEnum,
    WeightSensorMsgType,
)

logger = logging.getLogger(__name__)


class WebSocketClient(Thread):
    send_msg_queue: Queue[SendSchema] = Queue()

    def __init__(self, protocol, host, port, path, timeout, device_id):
        Thread.__init__(self)
        self.daemon = True
        self.url = f"{protocol}{host}:{port}{path}"
        self.timeout = timeout
        self.device_id = device_id
        self.ws = None
        self.lock = Lock()

    def connect(self):
        with self.lock:
            try:
                self.ws = connect(self.url, close_timeout=2)
                logger.info("Connected")
            except Exception as e:
                logger.error(f"Error: {e}")

    def send(self, op, topic=None, id=None, data=None):
        try:
            data = SendSchema(op=op, id=id, topic=topic, data=data)
            # bytes_data = data.json().encode()
            self.ws.send(data.json().encode())
            # logger.info(f"Sent: {data}")
        except Exception as e:
            logger.error(f"Error: {e}")

    def send_forward_distance(self):
        self.send(
            OperationEnum.publish,
            TopicEnum.forward_distance_sensor,
            None,
            ForwardDistanceSensorMsgType(
                distance=raybot.raybot_info.forward_distance
            ).model_dump(),
        )

    def send_backward_distance(self):
        self.send(
            OperationEnum.publish,
            TopicEnum.backward_distance_sensor,
            None,
            BackwardDistanceSensorMsgType(
                distance=raybot.raybot_info.backward_distance
            ).model_dump(),
        )

    def send_lift_distance(self):
        self.send(
            OperationEnum.publish,
            TopicEnum.lift_distance_sensor,
            None,
            LiftDistanceSensorMsgType(
                distance=raybot.raybot_info.lift_distance
            ).model_dump(),
        )

    def send_weight_sensor(self):
        self.send(
            OperationEnum.publish,
            TopicEnum.weight_sensor,
            None,
            WeightSensorMsgType(weight=raybot.raybot_info.weight).model_dump(),
        )

    def send_battery(self):
        self.send(
            OperationEnum.publish,
            TopicEnum.battery,
            None,
            BatteryMsgType(battery=raybot.raybot_info.battery).model_dump(),
        )

    def send_movement_motor(self):
        self.send(
            OperationEnum.publish,
            TopicEnum.movement_motor,
            None,
            MovementMotorMsgType(
                direction=raybot.raybot_info.movement_motor.__str__(),
                speed=raybot.raybot_info.movement_pwm,
            ).model_dump(),
        )

    def send_lift_motor(self):
        self.send(
            OperationEnum.publish,
            TopicEnum.lift_motor,
            None,
            LiftMotorMsgType(
                direction=raybot.raybot_info.lift_motor.__str__(),
                speed=raybot.raybot_info.lift_pwm,
            ).model_dump(),
        )

    def send_safety(self):
        self.send(
            OperationEnum.publish,
            TopicEnum.safety,
            None,
            SafetyMsgType(
                safety=raybot.raybot_info.safety, cause_by="Raybot safety system"
            ).model_dump(),
        )

    def send_door_state(self):
        self.send(
            OperationEnum.publish,
            TopicEnum.door_state,
            None,
            DoorStateMsgType(state=raybot.raybot_info.door_state).model_dump(),
        )

    def _handle_msg(self, data):
        try:
            data = CommandReciveSchema.model_validate_json(data)
            command_manager.add_command(data, self.response_command)
        except Exception as e:
            logger.error(f"Error: {e}")

    @classmethod
    def response_command(cls, command_id, name, status, msg):
        try:
            data = {"status": status}
            if msg:
                data.update(msg)
            if name:
                data.update({"name": name})
            cls.send_msg_queue.put(
                SendSchema(
                    op=OperationEnum.response,
                    id=command_id,
                    data=data,
                )
            )
        except WebSocketException as e:
            logger.error(f"Error: {e}")

    def send_to_server(self):
        """Gửi dữ liệu tới server (nếu có logic)."""
        while True:
            try:
                # Logic gửi dữ liệu
                # logger.info("Sending data to server...")
                if self.ws:
                    # self.send_forward_distance()
                    # self.send_backward_distance()
                    # self.send_lift_distance()
                    # self.send_weight_sensor()
                    # self.send_battery()
                    # self.send_movement_motor()
                    # self.send_lift_motor()
                    # self.send_safety()
                    # self.send_door_state()

                    if WebSocketClient.send_msg_queue.qsize() > 0:
                        data = WebSocketClient.send_msg_queue.get()
                        self.ws.send(json.dumps(data.model_dump()).encode())
                        logger.info(f"Sent: {data}")
                # else:
                #     logger.warning(
                #         "WebSocket not connected. Attempting to reconnect..."
                #     )
                #     self.connect()
                time.sleep(0.01)

            except (ConnectionClosed, ConnectionError, OSError):
                logger.warning(
                    "WebSocket connection closed during sending. Reconnecting..."
                )
                # self.ws = None  # Đặt lại kết nối

            except Exception as e:
                logger.error(f"Error while sending: {e}")

    def check_connection(self):
        while True:
            try:
                if self.ws:
                    # Gửi ping và chờ phản hồi pong
                    # WebSocketClient.send_msg_queue.put(
                    #     SendSchema(
                    #         op=OperationEnum.response,
                    #         id="aa86ecf1-85fe-4c49-8fa9-bc3f8f8b1d13",
                    #         data={"status": "ok", "name": f"ping-{uuid.uuid4()}"},
                    #     )
                    # )
                    pong_event = self.ws.ping()
                    pong_event.wait(timeout=5)  # Thời gian chờ là 5 giây

                    if pong_event.is_set():
                        # logger.info("Ping successful, pong received.")
                        pass
                    else:
                        logger.warning("Pong not received. Connection may be lost.")
                        raise ConnectionError("Pong response timeout.")
                else:
                    self.connect()

            except (ConnectionClosed, ConnectionError, OSError):
                logger.warning(
                    "WebSocket connection closed or pong failed. Reconnecting..."
                )
                self.ws = None  # Đặt lại kết nối
                self.connect()

            except Exception as e:
                logger.error(f"Unexpected error: {e}")

            sleep(1)  # Lặp lại kiểm tra sau mỗi 1 giây

    def listen_to_server(self):
        """Lắng nghe tin nhắn từ server qua WebSocket."""
        while True:
            try:
                if self.ws:
                    try:
                        logger.info("Listening to server...")
                        data = self.ws.recv()
                        if data:
                            logger.info(f"Received: {data}")
                            self._handle_msg(data)
                    except TimeoutError:
                        logging.warning("Timeout: No response from server")
                    except ConnectionClosed:
                        raise
                # sleep(0.01)
            except (ConnectionClosed, ConnectionError, OSError):
                logger.warning("WebSocket connection closed. Reconnecting...")
                # self.ws = None  # Đặt lại kết nối

            except Exception as e:
                logger.error(f"Unexpected error: {e}. Reconnecting...")
                # self.ws = None  # Đặt lại kết nối

    def run(self):
        t = Thread(target=self.send_to_server)
        t2 = Thread(target=self.check_connection)
        t.start()
        t2.start()
        self.listen_to_server()
        # while True:
        # self.send_forward_distance()
        # self.send_backward_distance()
        # self.send_lift_distance()
        # self.send_weight_sensor()
        # self.send_battery()
        # self.send_movement_motor()
        # self.send_lift_motor()
        # self.send_safety()
        # self.send_door_state()
        # sleep(self.timeout)
        # while True:
        #     try:
        #         if WebSocketClient.send_msg_queue.qsize() > 0:
        #             data = WebSocketClient.send_msg_queue.get()
        #             # self.ws.send(data.json().encode())
        #             self.ws.send(json.dumps(data.model_dump()).encode())
        #             logger.info(f"Sent: {data}")
        #         data = self.ws.recv()
        #         if data:
        #             logger.info(f"Recive: {data}")
        #             self.send_forward_distance()
        #             self._hanlde_msg(data)
        #             # self.ws.send("OK".encode())
        #     except Exception as e:
        #         logger.error(f"Error: {e}")
        #     sleep(0.001)

    def close(self):
        try:
            self.ws.close()
            logger.info("Closed")
        except Exception as e:
            logger.error(f"Error: {e}")

    def start(self):
        self.connect()
        retry = 0
        while retry < 3 and not self.ws:
            self.connect()
            retry += 1
            sleep(1)

        Thread.start(self)


logger = logging.getLogger(__name__)


class TopicPermission(Enum):
    READ = "read"
    WRITE = "write"
    READ_WRITE = "read_write"


class TopicManager:
    def __init__(self):
        self._topics: Dict[str, Dict[str, Any]] = {}
        self._subscriptions: Dict[str, Set[websockets.WebSocketServerProtocol]] = {}
        self.lock = threading.Lock()

    def register_topic(
        self, topic_name: str, permission: TopicPermission = TopicPermission.READ_WRITE
    ):
        """Register a new topic with specified permissions"""
        if topic_name not in self._topics:
            self._topics[topic_name] = {"permission": permission, "last_value": None}
            with self.lock:
                self._subscriptions[topic_name] = set()
            logger.info(
                f"Registered new topic: {topic_name} with permission {permission}"
            )

    def subscribe(
        self, topic_name: str, client: websockets.WebSocketServerProtocol
    ) -> bool:
        """Subscribe a client to a topic"""
        if topic_name not in self._topics:
            logger.warning(f"Attempt to subscribe to non-existent topic: {topic_name}")
            return False
        with self.lock:
            self._subscriptions[topic_name].add(client)
        logger.info(f"Client {id(client)} subscribed to topic: {topic_name}")
        return True

    def unsubscribe(
        self, topic_name: str, client: websockets.WebSocketServerProtocol
    ) -> bool:
        """Unsubscribe a client from a topic"""
        if (
            topic_name in self._subscriptions
            and client in self._subscriptions[topic_name]
        ):
            with self.lock:
                self._subscriptions[topic_name].remove(client)
            logger.info(f"Client {id(client)} unsubscribed from topic: {topic_name}")
            return True
        return False

    def get_subscribers(
        self, topic_name: str
    ) -> Set[websockets.WebSocketServerProtocol]:
        """Get all subscribers for a topic"""
        return self._subscriptions.get(topic_name, set())

    def can_publish(self, topic_name: str) -> bool:
        """Check if publishing to topic is allowed"""
        if topic_name not in self._topics:
            return False
        permission = self._topics[topic_name]["permission"]
        return permission in [TopicPermission.WRITE, TopicPermission.READ_WRITE]

    def can_subscribe(self, topic_name: str) -> bool:
        """Check if subscribing to topic is allowed"""
        if topic_name not in self._topics:
            return False
        permission = self._topics[topic_name]["permission"]
        return permission in [TopicPermission.READ, TopicPermission.READ_WRITE]

    def update_topic_value(self, topic_name: str, value: Any):
        """Update the last known value for a topic"""
        if topic_name in self._topics:
            self._topics[topic_name]["last_value"] = value

    def get_topic_value(self, topic_name: str) -> Any:
        """Get the last known value for a topic"""
        return self._topics.get(topic_name, {}).get("last_value")

    def get_all_topics(self) -> Dict[str, Dict]:
        """Get information about all registered topics"""
        return self._topics

    def remove_client(self, client: websockets.WebSocketServerProtocol):
        """Remove client from all subscriptions"""
        for topic in self._subscriptions.values():
            topic.discard(client)


class WebSocketServer(Thread):
    send_queue = Queue()

    def __init__(self, host, port):
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.clients = set()
        self.clients_lock = Lock()
        self.is_running = True
        self.topic_manager = TopicManager()
        self.server = None

        # Đăng ký các topic mặc định
        self._register_default_topics()

        # Khởi động các thread phụ
        self.state_thread = Thread(target=self._send_robot_state, daemon=True)
        self.queue_thread = Thread(target=self._process_send_queue, daemon=True)

    def _register_default_topics(self):
        """Register default topics for robot control and monitoring"""
        topics = [
            (TopicEnum.weight_sensor, TopicPermission.READ),
            (TopicEnum.movement_motor, TopicPermission.READ),
            (TopicEnum.lift_motor, TopicPermission.READ),
            (TopicEnum.command, TopicPermission.READ),
            (TopicEnum.forward_distance_sensor, TopicPermission.READ),
            (TopicEnum.backward_distance_sensor, TopicPermission.READ),
            (TopicEnum.battery, TopicPermission.READ),
            (TopicEnum.door_state, TopicPermission.READ),
            (TopicEnum.lift_distance_sensor, TopicPermission.READ),
            (TopicEnum.lift_pwm, TopicPermission.READ_WRITE),
            (TopicEnum.movement_pwm, TopicPermission.READ_WRITE),
            (TopicEnum.log, TopicPermission.READ),
            (TopicEnum.qr_location, TopicPermission.READ),
            (TopicEnum.qr_door, TopicPermission.READ),
            (TopicEnum.ram_cpu, TopicPermission.READ),
            (TopicEnum.safety, TopicPermission.READ),
            (TopicEnum.task, TopicPermission.READ),
        ]
        for topic, permission in topics:
            self.topic_manager.register_topic(topic, permission)

    def _handle_client(self, websocket):
        """Handle individual WebSocket client connection"""
        client_id = id(websocket)
        logger.info(f"New client connected: {client_id}")

        with self.clients_lock:
            self.clients.add(websocket)

        try:
            while self.is_running:
                try:
                    message = websocket.recv()
                    self._handle_message(websocket, message)
                    sleep(0.01)
                except ConnectionClosed:
                    break
                except Exception as e:
                    logger.error(f"Error handling message from client {client_id}: {e}")
                    self._send_error(websocket, str(e))

        finally:
            with self.clients_lock:
                self.clients.remove(websocket)
                self.topic_manager.remove_client(websocket)
            logger.info(f"Client disconnected: {client_id}")

    def _handle_message(self, websocket, message):
        """Process incoming messages from WebSocket clients"""
        try:
            res = CommandReciveSchema.model_validate_json(message)
            logger.info(f"Received from web client: {res}")

            if res.operation == OperationEnum.command:
                try:
                    logger.info(f"Received command: {res}")
                    command_manager.add_command(res, self.response_command)
                except Exception as e:
                    self._send_error(websocket, f"Invalid command: {str(e)}")

            elif res.operation == OperationEnum.subscribe:
                topic = res.data.get("topic")
                client_id = id(websocket)
                logger.info(f"Client {client_id} subscribing to topic: {topic}")

                if self.topic_manager.can_subscribe(topic):
                    if self.topic_manager.subscribe(topic, websocket):
                        logger.info(f"Subscribed client {client_id} to topic: {topic}")
                        self._send_message(
                            websocket,
                            {
                                "op": OperationEnum.subscribe,
                                "topic": topic,
                                "data": self.topic_manager.get_topic_value(topic),
                            },
                        )
                    else:
                        self._send_error(websocket, "Subscription failed")
                else:
                    self._send_error(websocket, "Cannot subscribe to this topic")

            elif res.operation == OperationEnum.unsubscribe:
                if self.topic_manager.unsubscribe(res.data["topic"], websocket):
                    self._send_message(
                        websocket,
                        {"op": OperationEnum.unsubscribe, "topic": res.data["topic"]},
                    )

        except Exception as e:
            self._send_error(websocket, f"Invalid message format: {str(e)}")

    def clean_data(self, data):
        if isinstance(data, dict):
            return {
                k: self.clean_data(v)
                for k, v in data.items()
                if not callable(v)  # Loại bỏ các method hoặc function
            }
        elif isinstance(data, list):
            return [self.clean_data(v) for v in data]
        elif isinstance(data, (str, int, float, bool, type(None))):
            return data
        elif hasattr(data, "value"):  # Xử lý Enum
            return data.value
        else:
            return str(data)  # Chuyển đối tượng khác thành chuỗi để log

    def _send_message(self, websocket, data):
        """Send a message to a WebSocket client"""
        try:
            # logger.info(f"Sending message to client {id(websocket)}: {data}")
            cleaned_data = self.clean_data(data)
            websocket.send(json.dumps(cleaned_data))

        except Exception as e:
            logger.error(f"Error sending message to client {id(websocket)}: {e}")
            with self.clients_lock:
                self.clients.remove(websocket)
                self.topic_manager.remove_client(websocket)

    def _send_error(self, websocket, message):
        """Send an error message to a WebSocket client"""
        self._send_message(websocket, {"op": OperationEnum.response, "data": message})

    @classmethod
    def response_command(cls, command_id, name, status, msg):
        """Handle command responses"""
        try:
            data = {"status": status}
            if msg:
                data.update(msg)
            if name:
                data.update({"name": name})
            cls.send_queue.put(
                SendSchema(
                    op=OperationEnum.response.value,
                    id=command_id,
                    data=data,
                    topic="command",
                )
            )
        except Exception as e:
            logger.error(f"Error in response command: {e}")

    def _send_robot_state(self):
        """Periodically broadcast robot state to subscribed clients"""
        while self.is_running:
            with self.clients_lock:
                if self.clients:
                    # logger.info("Broadcasting robot state to clients")
                    try:
                        # Collect robot state data

                        status = {"status": "ok"}
                        ram_cpu = {"ram_cpu": "0%"}
                        task = {"task": command_manager.get_current_command()}
                        command = {"command": raybot.raybot_info.current_cmd}
                        log = {"log": "No logs available"}
                        battery = {"battery": raybot.raybot_info.battery}
                        weight_sensor = {"weight_sensor": raybot.raybot_info.weight}
                        forward_distance_sensor = {
                            "forward_distance_sensor": raybot.raybot_info.forward_distance
                        }
                        backward_distance_sensor = {
                            "backward_distance_sensor": raybot.raybot_info.backward_distance
                        }
                        lift_distance_sensor = {
                            "lift_distance_sensor": raybot.raybot_info.lift_distance
                        }
                        movement_motor = {
                            "movement_motor": raybot.raybot_info.movement_motor
                        }
                        movement_pwm = {"movement_pwm": raybot.raybot_info.movement_pwm}
                        lift_motor = {"lift_motor": raybot.raybot_info.lift_motor}
                        lift_pwm = {"lift_pwm": raybot.raybot_info.lift_pwm}
                        safety = {"safety": raybot.raybot_info.safety}
                        qr_location = {"qr_location": raybot.raybot_info.qr_location}
                        qr_door = {"qr_door": raybot.raybot_info.qr_door}
                        door_state = {"door_state": raybot.raybot_info.door_state}

                        # Update topics and notify subscribers
                        all_data = {
                            **task,
                            **status,
                            **ram_cpu,
                            **command,
                            **log,
                            **battery,
                            **weight_sensor,
                            **forward_distance_sensor,
                            **backward_distance_sensor,
                            **lift_distance_sensor,
                            **movement_motor,
                            **movement_pwm,
                            **lift_motor,
                            **lift_pwm,
                            **safety,
                            **qr_location,
                            **qr_door,
                            **door_state,
                        }
                        for topic, value in all_data.items():
                            self.topic_manager.update_topic_value(topic, value)
                            message = {
                                "op": OperationEnum.publish,
                                "topic": topic,
                                "data": value,
                            }

                            for client in self.topic_manager.get_subscribers(topic):
                                try:
                                    self._send_message(client, message)
                                except Exception as e:
                                    logger.error(f"Error sending to subscriber: {e}")

                    except Exception as e:
                        logger.error(f"Error in robot state broadcast: {e}")

            time.sleep(1)

    def _process_send_queue(self):
        """Process messages in the send queue"""
        while self.is_running:
            try:
                if not self.send_queue.empty():
                    data = self.send_queue.get()
                    message = data.model_dump()

                    with self.clients_lock:
                        for client in self.clients:
                            self._send_message(client, message)

            except Exception as e:
                logger.error(f"Error processing send queue: {e}")

            time.sleep(0.01)

    def run(self):
        """Start the WebSocket server and all background threads"""
        try:
            logger.info(f"Starting WebSocket server on {self.host}:{self.port}")

            # Start background threads
            self.state_thread.start()
            self.queue_thread.start()

            # Start WebSocket server
            with serve(self._handle_client, self.host, self.port) as server:
                self.server = server
                self.server.serve_forever()
                logger.info("WebSocket server started")
                while self.is_running:
                    time.sleep(1)

        except Exception as e:
            logger.error(f"Error in WebSocket server: {e}")
            self.is_running = False
            raise

    def stop(self):
        """Stop the WebSocket server and all background threads"""
        logger.info("Stopping WebSocket server...")
        self.is_running = False
        if self.server:
            self.server.shutdown()
