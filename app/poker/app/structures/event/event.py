from typing import Callable

from schemas import WSEventSchema
from structures.exceptions import WSUnhandledEndpointError
from structures.handler import HandlerObject
from structures.helpers import CallbackType
from structures.ws import WSConnection


class EventObserver:
    def __init__(self) -> None:
        self.handlers: list[HandlerObject] = []

    def register(self, to_filter: str, callback: CallbackType) -> None:
        """
        Registers endpoint

        :param to_filter:
          filter to call endpoint
        :param callback:
          endpoint
        :return:
          None
        """
        to_add = HandlerObject(to_filter=to_filter, callback=callback)
        self.handlers.append(to_add)

    async def trigger(self, data: WSEventSchema, ws: WSConnection) -> None:
        """
        Calls the endpoint for the event

        :param data:
          received data from websocket connection
        :param ws:
          constructed websocket connection
        :return:
          None
        :raise WSUnhandledError:
          on unhandled event
        """

        for handler in self.handlers:
            check = handler.check(to_filter=data.payload.to_filter)

            if check:
                if handler.awaitable:
                    return await handler.callback(data=data, ws=ws)
                return handler.callback(data=data, ws=ws)
        raise WSUnhandledEndpointError(
            f"Endpoint with filter={data.payload.to_filter} doesn't exists"
        )

    def __call__(
        self,
        to_filter: str,
    ) -> Callable[[CallbackType], CallbackType]:
        """
        Used as a decorator to dynamically add an endpoint

        :param to_filter:
          filter to call endpoint
        :return:
          decorator
        """

        def wrapper(callback: CallbackType) -> CallbackType:
            self.register(to_filter=to_filter, callback=callback)
            return callback

        return wrapper
