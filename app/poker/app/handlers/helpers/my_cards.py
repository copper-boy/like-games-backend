from __future__ import annotations

from sqlalchemy import and_

from core import tools
from db.session import session as sessionmaker
from likeevents import LikeF, LikeRouter
from orm import CardModel
from schemas import EventSchema
from structures.enums import CardPositionEnum
from structures.ws import WS
from utils import helpers

router = LikeRouter()
path = "helperGetMyCards"


@router.like_helper(LikeF.path == path)
async def my_cards_handler(event: EventSchema, ws: WS) -> None:
    """
    Gets the player cards who called this method

    :param event:
      optional data received from client
    :param ws:
      constructed ws connection
    :return:
      None
    :raise WSStateError:
      when game not started
    """

    async with sessionmaker.begin() as session:
        await helpers.get_session_with_raise(session=session, session_id=ws.session_id)

        cards = await tools.store.card_accessor.get_cards_by(
            session=session,
            where=and_(
                CardModel.position == CardPositionEnum.player,
                CardModel.to_id == ws.player_id,
            ),
        )

    answer_event = EventSchema(
        path=path,
        payload={
            "data": helpers.cards_to_pydantic(cards=cards),
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
