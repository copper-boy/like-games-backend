from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi.websockets import WebSocket

from factory.base import BaseFactory
from structures.ws import WS

if TYPE_CHECKING:
    from ws import WSManager


class WSFactory(BaseFactory):
    def build(
        self,
        manager: WSManager,
        websocket: WebSocket,
        session_id: int,
        user_id: int,
        player_id: int,
    ) -> WS:
        """
        Constructs websocket connection

        :param manager:
          manager where stores connections
        :param websocket:
          websocket connection
        :param session_id:
          session id in database
        :param user_id:
          user if from user service
        :param player_id:
          created player id
        :return:
          constructed websocket connection
        """

        connection = WS(
            manager=manager,
            websocket=websocket,
            session_id=session_id,
            user_id=user_id,
            player_id=player_id,
        )

        return connection
