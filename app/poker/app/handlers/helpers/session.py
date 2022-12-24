from __future__ import annotations

from core import tools
from db.session import session as sessionmaker
from likeevents import LikeF, LikeRouter
from orm import SessionModel
from schemas import EventSchema, SessionSchema
from structures.ws import WS

router = LikeRouter()
path = "helperGetSession"


@router.like_helper(LikeF.path == path)
async def session_handler(event: EventSchema, ws: WS) -> None:
    """
    Returns the session the player is bound to

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
        s = await tools.store.game_session_accessor.get_session_by(
            session=session, where=(SessionModel.id == ws.session_id)
        )

    answer_event = EventSchema(
        path=path,
        payload={
            "data": SessionSchema.from_orm(s),
        },
    )
    await ws.manager.personal_json(event=answer_event, ws=ws)
