from __future__ import annotations

from typing import TYPE_CHECKING

from core import tools
from db.session import session as sessionmaker
from orm import SessionModel

if TYPE_CHECKING:
    from ws import WSManager

from .need_to_continue import need_to_continue
from .need_to_start import need_to_start


async def gamedef(manager: WSManager, session_id: int) -> None:
    async with sessionmaker.begin() as asyncsession:
        session = await tools.store.game_session_accessor.get_session_by(
            session=asyncsession, where=(SessionModel.id == session_id)
        )

    to_call = {
        True: need_to_continue,
        False: need_to_start,
    }

    await to_call[session.in_progress](manager=manager, session_id=session_id)
