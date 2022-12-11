from asyncio import Task
from typing import Any, Optional

from fastapi.websockets import WebSocket

from core import tools
from db.session import session
from misc import sch
from orm import PlayerModel
from schemas import WSEventSchema
from structures.exceptions import WSAlreadyConnectedError
from structures.ws import WSConnection
from tasks import gamedef_thread
from utils import helpers

from .base import BaseWSManager, BaseWSMessageManager


class WSManager(BaseWSManager, BaseWSMessageManager):
    def __init__(self) -> None:
        super(WSManager, self).__init__()
        self.start_session_task: Optional[Task] = None

        self.gamedef_schedule_task: Optional[Any] = None

        self.last_known_connected: int = 0

    @property
    def connected(self) -> int:
        return len(self._connections)

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
        except RuntimeError:
            ...

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
        manager = WSManager()
        self.managers[session_id] = manager

        manager.gamedef_schedule_task = sch.add_job(
            func=gamedef_thread, kwargs={"session_id": session_id}, trigger="interval", seconds=0.5
        )

        return self.managers[session_id]

    async def remove(self, session_id: int) -> None:
        exists = self.managers.get(session_id, None)
        if not exists:
            return None

        if not exists.connected:
            exists.gamedef_schedule_task.remove()
            self.managers.pop(session_id)

        async with session.begin() as asyncsession:
            players = await tools.store.game_player_accessor.get_players_by(
                session=asyncsession, where=(PlayerModel.session_id == session_id)
            )

        for player in players:
            await helpers.delete_player(
                manager=None, player_id=player.id, preview_balance=player.game_chips
            )
