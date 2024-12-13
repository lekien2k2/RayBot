# import logging
# from time import sleep

# # from app.database.sqlite.models.gateway_log import GatewayLog
# # from app.services.mqtt.service import LogMsg, MQTTService


# class LogDBHandler(logging.Handler):
#     def __init__(
#         self,
#         level: int,
#         chunk_size: int = 10,
#     ) -> None:
#         super().__init__(level)
#         self.chunk: list[GatewayLog] = []
#         self.chunk_size = chunk_size
#         self.counter = 0

#     def emit(self, record: logging.LogRecord) -> None:
#         """Emit log record."""
#         record.created = int(record.created * 1000)
#         self.chunk.append(
#             GatewayLog(
#                 ts=record.created,
#                 level=record.levelname,
#                 message=record.getMessage(),
#                 pathname=record.pathname,
#                 lineno=record.lineno,
#             )
#         )
#         from app.gateway import TBEGateway

#         if record.levelno >= logging.WARNING:
#             TBEGateway.log_queue.put(
#                 GatewayLog(
#                     ts=record.created,
#                     level=record.levelname,
#                     message=record.getMessage(),
#                     pathname=record.pathname,
#                     lineno=record.lineno,
#                 )
#             )

#         if record.levelno >= logging.ERROR:
#             priority = 1
#         elif record.levelno >= logging.WARNING:
#             priority = 3
#         else:
#             priority = 5

#         MQTTService.process_request_queue.put(
#             LogMsg(
#                 priority=priority,
#                 ts=record.created,
#                 log={
#                     "level": record.levelname,
#                     "message": record.getMessage(),
#                     "line": record.lineno,
#                     "path": record.pathname,
#                 },
#             )
#         )
#         # self.counter += 1
#         # if self.counter % self.chunk_size == 0:
#         #     self._insert_chunk()

#     def flush(self):
#         self._insert_chunk()

#     def _insert_chunk(self) -> None:
#         # TBEGateway.log_queue.put(self.chunk)
#         sleep(0.01)
