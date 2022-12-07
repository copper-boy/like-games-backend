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
        to_add = HandlerObject(to_filter=to_filter, callback=callback)
        self.handlers.append(to_add)

    async def trigger(self, data: WSEventSchema, ws: WSConnection) -> None:
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
        def wrapper(callback: CallbackType) -> CallbackType:
            self.register(to_filter=to_filter, callback=callback)
            return callback

        return wrapper
