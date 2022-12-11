from loguru import logger

from schemas import WSEventSchema
from structures.event import LikeEventObserver
from structures.exceptions import WSUnhandledEventError
from structures.ws import WSConnection


def _close_callback(ws: WSConnection) -> None:
    """
    Closes task for websocket connection

    :param ws:
      constructed websocket connection
    :return:
      None
    """

    if ws.timeout_task:
        ws.timeout_task.cancel()
        ws.timeout_task = None


class Router:
    def __init__(self) -> None:
        self.game = LikeEventObserver(event_name="game", callback=_close_callback)
        self.helper = LikeEventObserver(event_name="helper")

        self.observers: dict[str, LikeEventObserver] = {
            "game": self.game,
            "helper": self.helper,
        }

    async def event(self, data: WSEventSchema, ws: WSConnection) -> None:
        """
        Handle event from connection

        :param data:
          received data from websocket connection
        :param ws:
          constructed websocket connection
        :return:
          None
        :raise WSUnhandledEventError:
          on unhandled event
        """

        try:
            observer = self.observers[data.event]
        except KeyError as e:
            logger.exception(e)
            raise WSUnhandledEventError(f"Event with name={data.event} doesn't exists")

        await observer.trigger(data=data, ws=ws)
