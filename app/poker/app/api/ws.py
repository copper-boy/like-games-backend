from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.websockets import WebSocket, WebSocketDisconnect

from core import tools
from schemas import IntegrationUserSchema, WSEventSchema
from structures.ws import WSConnection

router = APIRouter()


async def _ws_endpoint(ws_connection: WSConnection) -> None:
    while True:
        event = await ws_connection.read()

        try:
            await tools.store.ws_accessor.handle(event=event, websocket=ws_connection.websocket)
        except:
            bad_event = WSEventSchema(command=event.command, payload={"message": "error"})
            await tools.ws_manager.personal_json(event=bad_event, connection=ws_connection)


@router.websocket(
    path="/ws",
)
async def ws(
    websocket: WebSocket,
    user: IntegrationUserSchema = Depends(
        tools.store.integration_user_accessor.get_user_websocket
    ),
) -> None:
    ws_connection = await tools.ws_manager.accept(websocket=websocket, user_id=user.id)

    await tools.ws_manager.broadcast_json(event=WSEventSchema(command="connect"))

    try:
        await _ws_endpoint(ws_connection=ws_connection)
    except WebSocketDisconnect:
        await tools.ws_manager.remove(user_id=user.id)

    await tools.ws_manager.broadcast_json(event=WSEventSchema(command="disconnect"))
