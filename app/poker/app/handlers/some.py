from core import tools
from schemas import WSEventSchema
from structures.ws import WSConnection


async def some_handler(event: WSEventSchema, websocket: WSConnection) -> None:
    tools.ws_manager.broadcast_json()
