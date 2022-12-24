from __future__ import annotations

from asyncio import Task
from typing import Any, Optional

from fastapi.websockets import WebSocket

from core import tools
from db.session import session
from misc import sch
from orm import PlayerModel
from schemas import EventSchema
from structures.exceptions import WSAlreadyConnectedError
from structures.ws import WS
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
        return len(self._wss)

    async def accept(
        self, websocket: WebSocket, session_id: int, user_id: int, player_id: int
    ) -> WS:
        await websocket.accept()

        is_connected = self.ws(user_id=user_id)
        if is_connected:
            raise WSAlreadyConnectedError

        ws = tools.factory.ws_factory.build(
            manager=self,
            websocket=websocket,
            session_id=session_id,
            user_id=user_id,
            player_id=player_id,
        )
        ws.manager = self
        self._wss[user_id] = ws

        return ws

    def remove(self, user_id: int) -> None:
        self._wss.pop(user_id)

    def ws(self, user_id: int) -> WS:
        ws = self._wss.get(user_id)

        return ws

    async def broadcast_json(self, event: EventSchema) -> None:
        to_dict = event.dict()
        for user_id, ws in self._wss.items():
            try:
                await ws.websocket.send_json(data=to_dict)
            except RuntimeError:
                self.remove(user_id=user_id)

    async def personal_json(self, event: EventSchema, ws: WS) -> None:
        to_dict = event.dict()

        try:
            await ws.websocket.send_json(data=to_dict)
        except RuntimeError:
            self.remove(user_id=ws.user_id)


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

        return manager

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
                player=player, user_id=player.user_id, preview_balance=player.game_chips
            )
