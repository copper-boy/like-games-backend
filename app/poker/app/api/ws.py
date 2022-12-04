from fastapi import APIRouter
from fastapi.param_functions import Depends, Path
from fastapi.websockets import WebSocket, WebSocketDisconnect
from loguru import logger
from starlette import status

from core import tools
from db.session import session as sessionmaker
from schemas import IntegrationUserSchema, WSEventSchema
from structures.exceptions import WSAlreadyConnectedError
from structures.ws import WSConnection
from utils import helpers
from ws import WSManager

router = APIRouter()


async def _ws_endpoint(manager: WSManager, ws_connection: WSConnection) -> None:
    while True:
        event = await ws_connection.read()

        try:
            await tools.store.ws_accessor.handle(event=event, websocket=ws_connection)
        except Exception as e:
            logger.exception(e)
            bad_event = WSEventSchema(command=event.command, payload={"message": "error"})
            await manager.personal_json(event=bad_event, connection=ws_connection)


@router.websocket(
    path="/ws/{session_id}",
)
async def ws(
    websocket: WebSocket,
    session_id: int = Path(...),
    iuser: IntegrationUserSchema = Depends(
        tools.store.integration_user_accessor.get_user_websocket
    ),
) -> None:
    try:
        manager = tools.ws_managers.get(session_id=session_id)
        ws_connection = await manager.accept(
            websocket=websocket, user_id=iuser.id, session_id=session_id
        )
    except WSAlreadyConnectedError as e:
        logger.exception(e)
        return await websocket.close(
            code=status.WS_1013_TRY_AGAIN_LATER,
            reason="already connected",
        )

    async with sessionmaker.begin() as session:
        await helpers.delete_player(session=session, user_id=iuser.id)
    async with sessionmaker.begin() as session:
        player = await helpers.create_player(
            session=session, session_id=session_id, user_id=iuser.id
        )
    ws_connection.player_id = player.id

    await manager.broadcast_json(event=WSEventSchema(command="connect"))

    try:
        await _ws_endpoint(manager=manager, ws_connection=ws_connection)
    except WebSocketDisconnect as e:
        logger.exception(e)
        await manager.remove(user_id=iuser.id)

    await manager.broadcast_json(event=WSEventSchema(command="disconnect"))
