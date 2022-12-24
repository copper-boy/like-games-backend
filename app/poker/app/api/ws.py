from fastapi import APIRouter
from fastapi.param_functions import Depends, Path
from fastapi.websockets import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError

from core import tools
from handlers import router as handlers_router
from likeevents import LikeRootRouter
from likeevents.liketypes import LikeTriggerResponseNamedTuple
from orm import PlayerModel
from schemas import EventSchema, IntegrationPotUpdateSchema, IntegrationUserSchema
from structures.ws import WS
from utils import helpers
from ws import WSManager

router = APIRouter()
like_router = LikeRootRouter()
like_router.include_router(handlers_router)


@like_router.like_update()
async def like_update(update: EventSchema, **kwargs: dict) -> LikeTriggerResponseNamedTuple:
    return await like_router.event(update_type=update.type, event=update, **kwargs)


async def ___ws_endpoint(ws: WS) -> None:
    """
    Websocket endpoint third level

    :param ws:
      constructed websocket connection
    :return:
      None
    """

    await like_router.start_listen(updates_from=ws.read(), ws=ws)


async def __ws_endpoint(
    manager: WSManager,
    websocket: WebSocket,
    session_id: int,
    iuser: IntegrationUserSchema,
    player: PlayerModel,
) -> None:
    ws = await manager.accept(
        websocket=websocket, session_id=session_id, user_id=iuser.id, player_id=player.id
    )

    try:
        await ___ws_endpoint(ws=ws)
    except WebSocketDisconnect:
        manager.remove(user_id=ws.user_id)
    except ConnectionClosedError:
        manager.remove(user_id=ws.user_id)
    except Exception:
        manager.remove(user_id=ws.user_id)


async def _ws_endpoint(
    manager: WSManager,
    websocket: WebSocket,
    session_id: int,
    iuser: IntegrationUserSchema,
) -> None:
    """
    Websocket endpoint second level.

    :param websocket:
      websocket connection
    :param session_id:
      session id need to connect to the game
    :param iuser:
      user object from user service
    :param manager:
      manager for session
    :return:
      None
    """

    pot = await tools.store.integration_pot_accessor.get_pot(user_id=iuser.id)

    new_balance, player = await helpers.new_player(
        session_id=session_id,
        user_id=iuser.id,
        pot=pot.pot,
    )
    to_update = IntegrationPotUpdateSchema(pot=new_balance)
    await tools.store.integration_pot_accessor.update_pot(user_id=iuser.id, json=to_update)

    try:
        await __ws_endpoint(
            manager=manager, websocket=websocket, session_id=session_id, iuser=iuser, player=player
        )
    finally:
        await helpers.delete_player(
            player=player,
            user_id=iuser.id,
            preview_balance=new_balance,
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
    """
    Websocket endpoint first level.

    :param websocket:
      websocket connection
    :param session_id:
      session id need to connect to the game
    :param iuser:
      user object from user service
    :return:
      None
    """
    manager = tools.ws_managers.get(session_id=session_id)

    try:
        await _ws_endpoint(
            manager=manager, websocket=websocket, session_id=session_id, iuser=iuser
        )
    finally:
        await tools.ws_managers.remove(session_id=session_id)
