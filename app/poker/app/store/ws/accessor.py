from typing import Awaitable, Callable, TypeVar

from schemas import WSEventSchema
from store.base import BaseAccessor
from structures.ws import WSConnection

AsyncCallable = TypeVar(
    "AsyncCallable", bound=Callable[[WSConnection, WSEventSchema], Awaitable[...]]
)


class WSAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs) -> None:
        super(WSAccessor, self).__init__(*args, **kwargs)

        self.handlers: dict[str, AsyncCallable] = {}

    def register_handler(self, command: str, function: AsyncCallable) -> None:
        self.handlers[command] = function

    async def handle(self, event: WSEventSchema, websocket: WSConnection) -> None:
        command_handler = self.handlers[event.command]
        await command_handler(event=event, websocket=websocket)
