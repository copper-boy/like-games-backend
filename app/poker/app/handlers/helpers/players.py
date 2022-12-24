from __future__ import annotations

from core import tools
from db.session import session as sessionmaker
from likeevents import LikeF, LikeRouter
from orm import PlayerModel
from schemas import EventSchema
from structures.ws import WS
from utils import helpers

router = LikeRouter()
path = "helperGetPlayers"


@router.like_helper(LikeF.path == path)
async def players_handler(event: EventSchema, ws: WS) -> None:
    """
    Gets the players in the game

    :param event:
      required data received from client
    :param ws:
      constructed ws connection
    :return:
      None
    """

    async with sessionmaker.begin() as session:
        players = await tools.store.game_player_accessor.get_players_by(
            session=session, where=(PlayerModel.session_id == ws.session_id)
        )

    answer_event = EventSchema(
        path=path,
        payload={
            "data": helpers.players_to_pydantic(players=players, exclude=ws.player_id),
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
