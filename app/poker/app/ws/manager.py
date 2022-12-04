from fastapi.websockets import WebSocket

from core import tools
from schemas import WSEventSchema
from structures.exceptions import WSAlreadyConnectedError
from structures.ws import WSConnection

from .base import BaseWSManager, BaseWSMessageManager


class WSManager(BaseWSManager, BaseWSMessageManager):
    def __init__(self) -> None:
        super(WSManager, self).__init__()

    async def accept(self, session_id: int, websocket: WebSocket, user_id: int) -> WSConnection:
        await websocket.accept()

        is_connected = self.connection(user_id=user_id)
        if is_connected:
            raise WSAlreadyConnectedError

        connection = tools.factory.connection_factory.build(
            session_id=session_id, websocket=websocket, user_id=user_id
        )
        self._connections[user_id] = connection

        return connection

    async def remove(self, user_id: int) -> None:
        ws_connection = self._connections.pop(user_id)
        await ws_connection.websocket.close()

    def connection(self, user_id: int) -> WSConnection:
        connection = self._connections.get(user_id)

        return connection

    async def broadcast_json(self, event: WSEventSchema) -> None:
        to_dict = event.dict()
        for user_id in self._connections:
            connection = self.connection(user_id=user_id)
            await connection.websocket.send_json(data=to_dict)

    async def personal_json(self, event: WSEventSchema, connection: WSConnection) -> None:
        to_dict = event.dict()

        await connection.websocket.send_json(data=to_dict)


class WSManagerList:
    def __init__(self) -> None:
        self.managers: dict[int, WSManager] = {}

    def get(self, session_id: int) -> WSManager:
        exists = self.managers.get(session_id, None)
        if exists:
            return exists
        self.managers[session_id] = WSManager()
        return self.managers[session_id]
