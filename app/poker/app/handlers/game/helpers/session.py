from db.session import session as sessionmaker
from misc import router
from schemas import SessionSchema, WSEventSchema
from structures.ws import WSConnection
from utils import helpers


@router.game(to_filter="session")
async def session_handler(data: WSEventSchema, ws: WSConnection) -> None:
    async with sessionmaker.begin() as session:
        s = await helpers.get_session_with_raise(session=session, session_id=ws.session_id)

    answer_event = WSEventSchema(
        event="game",
        payload={
            "to_filter": "session",
            "data": SessionSchema.from_orm(s),
        },
    )
    await ws.manager.personal_json(event=answer_event, connection=ws)
