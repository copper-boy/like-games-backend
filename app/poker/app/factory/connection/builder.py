from fastapi.websockets import WebSocket

from factory.base import BaseFactory
from structures.ws import WSConnection


class ConnectionFactory(BaseFactory):
    def build(self, websocket: WebSocket, user_id: int) -> WSConnection:
        connection = WSConnection(websocket=websocket, user_id=user_id)

        return connection
