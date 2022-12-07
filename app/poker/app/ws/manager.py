from asyncio import Task
from typing import Optional

from fastapi.websockets import WebSocket
from loguru import logger

from core import tools
from schemas import WSEventSchema
from structures.exceptions import WSAlreadyConnectedError
from structures.ws import WSConnection

from .base import BaseWSManager, BaseWSMessageManager


class WSManager(BaseWSManager, BaseWSMessageManager):
    def __init__(self) -> None:
        super(WSManager, self).__init__()

        self.start_session_task: Optional[Task] = None

    async def accept(self, session_id: int, websocket: WebSocket, user_id: int) -> WSConnection:
        await websocket.accept()

        is_connected = self.connection(user_id=user_id)
        if is_connected:
            raise WSAlreadyConnectedError

        connection = tools.factory.connection_factory.build(
            session_id=session_id, websocket=websocket, user_id=user_id
        )
        connection.manager = self
        self._connections[user_id] = connection

        return connection

    async def remove(self, user_id: int) -> None:
        ws_connection = self._connections.pop(user_id)
        try:
            await ws_connection.websocket.close()
        except RuntimeError as e:
            logger.exception(e)

    def connection(self, user_id: int) -> WSConnection:
        connection = self._connections.get(user_id)

        return connection

    async def broadcast_json(self, event: WSEventSchema) -> None:
        to_dict = event.dict()
        for user_id, connection in self._connections.items():
            try:
                await connection.websocket.send_json(data=to_dict)
            except RuntimeError:
                self._connections.pop(user_id)

    async def personal_json(self, event: WSEventSchema, connection: WSConnection) -> None:
        to_dict = event.dict()

        try:
            await connection.websocket.send_json(data=to_dict)
        except RuntimeError:
            self._connections.pop(connection.user_id)


class WSManagerList:
    def __init__(self) -> None:
        self.managers: dict[int, WSManager] = {}

    def get(self, session_id: int) -> WSManager:
        exists = self.managers.get(session_id, None)
        if exists:
            return exists
        self.managers[session_id] = WSManager()
        return self.managers[session_id]
