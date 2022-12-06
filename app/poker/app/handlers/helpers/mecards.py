from sqlalchemy import and_

from core import tools
from db.session import session as sessionmaker
from misc import router
from orm import CardModel
from schemas import WSEventSchema
from structures.enums import CardPositionEnum
from structures.ws import WSConnection
from utils import helpers


@router.helper(to_filter="mecards")
async def mecards_handler(data: WSEventSchema, ws: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        await helpers.get_session_with_raise(session=session, session_id=ws.session_id)

        cards = await tools.store.card_accessor.get_cards_by(
            session=session,
            where=and_(
                CardModel.position == CardPositionEnum.player,
                CardModel.to_id == ws.player_id,
            ),
        )

    answer_event = WSEventSchema(
        event="helper",
        payload={
            "to_filter": "mecards",
            "data": helpers.cards_to_pydantic(cards=cards),
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
