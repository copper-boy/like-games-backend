from __future__ import annotations

from abc import ABC, abstractmethod

from fastapi.websockets import WebSocket

from schemas import EventSchema
from structures.ws import WS


class BaseWSManager(ABC):
    def __init__(self) -> None:
        self._wss: dict[int, WS] = {}

    @abstractmethod
    async def accept(
        self, websocket: WebSocket, session_id: int, user_id: int, player_id: int
    ) -> WS:
        ...

    @abstractmethod
    def remove(self, user_id: int) -> None:
        ...

    @abstractmethod
    def ws(self, user_id: int) -> WS:
        ...


class BaseWSMessageManager(ABC):
    @abstractmethod
    async def broadcast_json(self, event: EventSchema) -> None:
        ...

    @abstractmethod
    async def personal_json(self, event: EventSchema, ws: WS) -> None:
        ...
