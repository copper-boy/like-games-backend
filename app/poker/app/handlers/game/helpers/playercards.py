from sqlalchemy import and_

from core import tools
from db.session import session as sessionmaker
from misc import router
from orm import CardModel
from schemas import WSEventSchema
from structures.enums import CardPositionEnum, RoundTypeEnum
from structures.exceptions import WSCommandError
from structures.ws import WSConnection
from utils import helpers


@router.game(to_filter="playercards")
async def playercards_handler(data: WSEventSchema, ws: WSConnection) -> None:
    player_id = data.payload.data.get("player_id")

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
            if not cards:
                raise WSCommandError
        else:
            raise WSCommandError

    answer_event = WSEventSchema(
        event="game",
        payload={
            "to_filter": "playercards",
            "data": helpers.cards_to_pydantic(cards=cards),
        },
    )
    await ws.manager.broadcast_json(event=answer_event)
