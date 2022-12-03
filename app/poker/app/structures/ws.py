from asyncio import Task

from fastapi.websockets import WebSocket

from schemas import WSEventSchema


class BaseWSConnection:
    websocket: WebSocket


class BaseMetaTimeoutTask(type):
    timeout_task: Task | None = None


class MetaTimeoutTask(BaseMetaTimeoutTask):
    def __new__(cls, *args, **kwargs) -> ...:
        to_return = super().__new__(cls, *args, **kwargs)
        to_return.timeout_task = None

        return to_return


class WSConnection(BaseWSConnection, metaclass=MetaTimeoutTask):
    user_id: int

    async def read(self) -> WSEventSchema:
        json = await self.websocket.receive_json()

        return WSEventSchema.parse_obj(json)
