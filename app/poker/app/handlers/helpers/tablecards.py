from sqlalchemy import and_

from core import tools
from db.session import session as sessionmaker
from misc import router
from orm import CardModel
from schemas import WSEventSchema
from structures.enums import CardPositionEnum
from structures.ws import WSConnection
from utils import helpers


@router.helper(to_filter="tablecards")
async def tablecards_handler(data: WSEventSchema, ws: WSConnection) -> None:
    """
    Returns the table cards

    :param data:
      optional data received from client
    :param ws:
      constructed websocket connection
    :return:
      None
    :raise WSStateError:
      when game not started
    """

    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)

        cards = await tools.store.card_accessor.get_cards_by(
            session=session,
            where=and_(
                CardModel.position == CardPositionEnum.table,
                CardModel.deck_id == s.deck_id,
            ),
        )

    answer_event = WSEventSchema(
        event="game",
        payload={
            "to_filter": "mecards",
            "data": helpers.cards_to_pydantic(cards=cards),
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
