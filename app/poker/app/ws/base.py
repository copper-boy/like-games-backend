from abc import ABC, abstractmethod

from fastapi.websockets import WebSocket

from schemas import WSEventSchema
from structures.ws import WSConnection


class BaseWSManager(ABC):
    def __init__(self) -> None:
        self._connections: dict[int, WSConnection] = {}

    @abstractmethod
    async def accept(self, websocket: WebSocket, user_id: int) -> WSConnection:
        ...

    @abstractmethod
    async def remove(self, user_id: int) -> None:
        ...

    @abstractmethod
    def connection(self, user_id: int) -> WSConnection:
        ...


class BaseWSMessageManager(ABC):
    @abstractmethod
    async def broadcast_json(self, event: WSEventSchema) -> None:
        ...

    @abstractmethod
    async def personal_json(self, event: WSEventSchema, connection: WSConnection) -> None:
        ...
