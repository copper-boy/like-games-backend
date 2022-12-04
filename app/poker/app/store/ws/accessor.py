from typing import Awaitable, Callable, TypeVar

from schemas import WSEventSchema
from store.base import BaseAccessor
from structures.command import Command
from structures.exceptions import WSCommandError
from structures.ws import WSConnection

AsyncCallable = TypeVar(
    "AsyncCallable", bound=Callable[[WSConnection, WSEventSchema], Awaitable[...]]
)


class WSAccessor(BaseAccessor):
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super(WSAccessor, self).__init__(*args, **kwargs)

        self.handlers: dict[Command, AsyncCallable] = {}

    def register_handler(self, command: Command, function: AsyncCallable) -> None:
        self.handlers[command] = function

    async def handle(self, event: WSEventSchema, websocket: WSConnection) -> None:
        for handler, function in self.handlers.items():
            if handler.command == event.command:
                return await function(event=event, websocket=websocket)
        raise WSCommandError
