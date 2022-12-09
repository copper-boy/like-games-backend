from core import tools
from db.session import session as sessionmaker
from orm import SessionModel

from .need_to_continue import need_to_continue
from .need_to_start import need_to_start


async def gamedef(manager, session_id: int) -> None:
    async with sessionmaker.begin() as asyncsession:
        session = await tools.store.game_session_accessor.get_session_by(
            session=asyncsession, where=(SessionModel.id == session_id)
        )

    to_call = {
        True: need_to_continue,
        False: need_to_start,
    }

    await to_call[session.in_progress](manager=manager, session_id=session_id)
