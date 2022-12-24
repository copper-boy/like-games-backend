from __future__ import annotations

from asyncio import Task
from dataclasses import dataclass
from typing import TYPE_CHECKING, AsyncIterable, Optional

from fastapi.websockets import WebSocket

from schemas import EventSchema

if TYPE_CHECKING:
    from ws import WSManager


class MetaTimeoutTask(type):
    def __new__(cls, *args: tuple, **kwargs: dict) -> MetaTimeoutTask:
        to_return = super(MetaTimeoutTask, cls).__new__(cls, *args, **kwargs)
        to_return.timeout_task: Optional[Task] = None  # noqa

        return to_return


@dataclass
class WS(metaclass=MetaTimeoutTask):
    manager: WSManager
    websocket: WebSocket

    session_id: int

    user_id: int
    player_id: Optional[int] = None

    async def read(self) -> AsyncIterable[EventSchema]:
        while True:
            json = await self.websocket.receive_json()
            yield EventSchema.parse_obj(json)
