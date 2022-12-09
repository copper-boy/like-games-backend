from asyncio import Task
from dataclasses import dataclass
from typing import Any, Optional

from fastapi.websockets import WebSocket

from schemas import WSEventSchema


@dataclass
class BaseWSConnection:
    websocket: WebSocket


class MetaTimeoutTask(type):
    def __new__(cls, *args: tuple, **kwargs: dict) -> ...:
        to_return = super().__new__(cls, *args, **kwargs)
        to_return.timeout_task: Optional[Task] = None  # noqa

        return to_return


@dataclass
class WSConnection(BaseWSConnection, metaclass=MetaTimeoutTask):
    session_id: int
    user_id: int
    manager: Any = None
    player_id: int | None = None

    async def read(self) -> WSEventSchema:
        json = await self.websocket.receive_json()

        return WSEventSchema.parse_obj(json)
