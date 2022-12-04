from sqlalchemy import and_

from core import tools
from db.session import session as sessionmaker
from orm import CardModel, RoundModel, SessionModel
from schemas import PlayercardsPayloadSchema, WSEventSchema
from structures.enums import CardPositionEnum, RoundTypeEnum
from structures.exceptions import WSCommandError
from structures.ws import WSConnection
from utils import helpers


async def playercards_handler(event: WSEventSchema, websocket: WSConnection) -> None:
    payload = PlayercardsPayloadSchema.parse_obj(event.payload)

    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=websocket.session_id)

        if s.round.type == RoundTypeEnum.showdown or websocket.player_id == payload.player_id:
            cards = await tools.store.card_accessor.get_cards_by(
                session=session,
                where=and_(
                    CardModel.position == CardPositionEnum.player,
                    CardModel.to_id == payload.player_id,
                ),
            )
            if not cards:
                raise WSCommandError
        else:
            raise WSCommandError

    player_cards = helpers.cards_to_pydantic(cards=cards)
    answer_event = WSEventSchema(command=event.command, payload={"cards": player_cards})
    manager = tools.ws_managers.get(websocket.session_id)
    await manager.personal_json(event=answer_event, connection=websocket)
