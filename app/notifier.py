from queue import Queue
from typing import TypeVar

TData = TypeVar("TData")


class EventNotifier[TData]:
    def __init__(self):
        self._queues: list[Queue[TData]] = []

    def create_queue_listener(self) -> Queue[TData]:
        queue = Queue[TData]()
        self._queues.append(queue)
        return queue

    def remove_queue_listener(self, subscriber: Queue[TData]) -> None:
        if subscriber in self._queues:
            self._queues.remove(subscriber)

    def dispatch(self, data: TData) -> None:
        for subscriber in self._queues:
            subscriber.put(data)
