from fastapi import APIRouter
from fastapi.param_functions import Depends, Path
from fastapi.websockets import WebSocket, WebSocketDisconnect
from loguru import logger
from starlette import status
from websockets.exceptions import ConnectionClosedError

from core import tools
from misc import router as ws_router
from schemas import IntegrationPotUpdateSchema, IntegrationUserSchema, WSEventSchema
from structures.enums import WSEventEnum
from structures.exceptions import (
    BaseWSError,
    WSAlreadyConnectedError,
    WSCommandError,
    WSConnectionError,
    WSStateError,
    WSUnhandledEndpointError,
    WSUnhandledEventError,
)
from structures.ws import WSConnection
from utils import gamedef, helpers

router = APIRouter()


async def _ws_endpoint(ws_connection: WSConnection) -> None:
    await gamedef.gamedef(manager=ws_connection.manager, session_id=ws_connection.session_id)

    while True:
        data = await ws_connection.read()

        try:
            await ws_router.event(data=data, ws=ws_connection)
        except WSUnhandledEndpointError as e:
            bad_event = WSEventSchema(
                event=WSEventEnum.error,
                payload={
                    "to_filter": data.payload.to_filter,
                    "data": {
                        "exception": str(e),
                        "exception_name": e.__class__.__name__.lower(),
                    },
                },
            )
            await ws_connection.manager.personal_json(event=bad_event, connection=ws_connection)
        except WSUnhandledEventError as e:
            logger.exception(e)
            bad_event = WSEventSchema(
                event=WSEventEnum.error,
                payload={
                    "to_filter": data.payload.to_filter,
                    "data": {
                        "exception": str(e),
                        "exception_name": e.__class__.__name__.lower(),
                    },
                },
            )
            await ws_connection.manager.personal_json(event=bad_event, connection=ws_connection)
        except WSCommandError as e:
            logger.exception(e)
            bad_event = WSEventSchema(
                event=WSEventEnum.error,
                payload={
                    "to_filter": data.payload.to_filter,
                    "data": {
                        "exception": str(e),
                        "exception_name": e.__class__.__name__.lower(),
                    },
                },
            )
            await ws_connection.manager.personal_json(event=bad_event, connection=ws_connection)
        except BaseWSError as e:
            logger.exception(e)
            bad_event = WSEventSchema(
                event=WSEventEnum.error,
                payload={
                    "to_filter": data.payload.to_filter,
                    "data": {
                        "exception": str(e),
                        "exception_name": e.__class__.__name__.lower(),
                    },
                },
            )
            await ws_connection.manager.personal_json(event=bad_event, connection=ws_connection)
        except Exception as e:
            logger.exception(e)
            bad_event = WSEventSchema(
                event=WSEventEnum.server_error,
                payload={
                    "to_filter": data.payload.to_filter,
                    "data": {
                        "exception": "Exception detail not allowed in server exceptions",
                        "exception_name": "Exception name not allowed in server exceptions",
                    },
                },
            )
            await ws_connection.manager.personal_json(event=bad_event, connection=ws_connection)
        else:
            match data.event:
                case WSEventEnum.game:
                    await gamedef.gamedef(
                        manager=ws_connection.manager, session_id=ws_connection.session_id
                    )


@router.websocket(
    path="/ws/{session_id}",
)
async def ws_endpoint(
    websocket: WebSocket,
    session_id: int = Path(...),
    iuser: IntegrationUserSchema = Depends(
        tools.store.integration_user_accessor.get_user_websocket
    ),
) -> None:
    pot = await tools.store.integration_pot_accessor.get_pot(user_id=iuser.id)

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
    try:
        new_balance, player = await helpers.new_player(
            manager=ws_connection.manager,
            session_id=ws_connection.session_id,
            user_id=ws_connection.user_id,
            pot=pot.pot,
        )
    except WSConnectionError as e:
        logger.exception(e)
        bad_event = WSEventSchema(
            event=WSEventEnum.error,
            payload={
                "data": {
                    "exception": str(e),
                    "exception_name": e.__class__.__name__.lower(),
                },
            },
        )
        await ws_connection.manager.personal_json(event=bad_event, connection=ws_connection)

        return await manager.remove(user_id=ws_connection.user_id)
    except WSStateError as e:
        logger.exception(e)
        return await websocket.close(
            code=status.WS_1013_TRY_AGAIN_LATER,
            reason="unable to join",
        )
    else:
        to_update = IntegrationPotUpdateSchema(pot=new_balance)
        await tools.store.integration_pot_accessor.update_pot(user_id=iuser.id, json=to_update)

    ws_connection.player_id = player.id

    try:
        await _ws_endpoint(ws_connection=ws_connection)
    except WebSocketDisconnect as e:
        logger.exception(e)
        await manager.remove(user_id=ws_connection.user_id)
    except ConnectionClosedError as e:
        logger.exception(e)
        await manager.remove(user_id=ws_connection.user_id)
    except Exception:
        await manager.remove(user_id=ws_connection.user_id)

    await helpers.delete_player(
        manager=ws_connection.manager,
        player_id=ws_connection.player_id,
        preview_balance=new_balance,
    )
