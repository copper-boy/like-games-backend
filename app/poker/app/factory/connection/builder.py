from fastapi.websockets import WebSocket

from factory.base import BaseFactory
from structures.ws import WSConnection


class ConnectionFactory(BaseFactory):
    def build(self, session_id: int, websocket: WebSocket, user_id: int) -> WSConnection:
        """
        Constructs websocket connection

        :param session_id:
          session id in database
        :param websocket:
          websocket connection
        :param user_id:
          user if from user service
        :return:
          constructed websocket connection
        """

        connection = WSConnection(session_id=session_id, websocket=websocket, user_id=user_id)

        return connection
