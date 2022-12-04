from sqlalchemy import and_

from core import tools
from db.session import session as sessionmaker
from orm import CardModel
from schemas import WSEventSchema
from structures.enums import CardPositionEnum
from structures.ws import WSConnection
from utils import helpers


async def mecards_handler(event: WSEventSchema, websocket: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        await helpers.get_session_with_raise(session=session, session_id=websocket.session_id)

        cards = await tools.store.card_accessor.get_cards_by(
            session=session,
            where=and_(
                CardModel.position == CardPositionEnum.player,
                CardModel.to_id == websocket.player_id,
            ),
        )

    player_cards = helpers.cards_to_pydantic(cards=cards)
    answer_event = WSEventSchema(command=event.command, payload={"cards": player_cards})
    manager = tools.ws_managers.get(websocket.session_id)
    await manager.personal_json(event=answer_event, connection=websocket)
