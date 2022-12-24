from __future__ import annotations

from sqlalchemy import and_

from core import tools
from db.session import session as sessionmaker
from likeevents import LikeF, LikeRouter
from orm import CardModel
from schemas import EventSchema
from structures.enums import CardPositionEnum, RoundTypeEnum
from structures.exceptions import WSCommandError
from structures.ws import WS
from utils import helpers

router = LikeRouter()
path = "helperGeyPlayerCards"


@router.like_helper(LikeF.path == path)
async def player_cards_handler(event: EventSchema, ws: WS) -> None:
    """
    Gets the player cards by player id

    :param event:
      required data received from client
    :param ws:
      constructed ws connection
    :return:
      None
    :raise WSCommandError:
      when round type not equals `RoundTypeEnum.showdown`
    :raise WSStateError:
      when game not started
    """

    player_id = event.payload.data.get("player_id")

    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)

        if s.round.type == RoundTypeEnum.showdown:
            cards = await tools.store.card_accessor.get_cards_by(
                session=session,
                where=and_(
                    CardModel.position == CardPositionEnum.player,
                    CardModel.to_id == player_id,
                ),
            )
        else:
            raise WSCommandError

    answer_event = EventSchema(
        path=path,
        payload={
            "to_filter": "playercards",
            "data": helpers.cards_to_pydantic(cards=cards),
        },
    )
    await ws.manager.personal_json(event=answer_event, ws=ws)
