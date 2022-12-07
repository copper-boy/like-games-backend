import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from db.session import session as sessionmaker
from orm import GameModel, RoundModel, SessionModel
from schemas import WSEventSchema
from structures.enums import RoundTypeEnum
from utils import helpers
from ws import WSManager


async def _showdown(session: AsyncSession, manager: WSManager, s: SessionModel) -> None:
    ...


async def gamedef(manager: WSManager, session_id: int) -> None:
    async with sessionmaker.begin() as asyncsession:
        session = await tools.store.game_session_accessor.get_session_by(
            session=asyncsession, where=(SessionModel.id == session_id)
        )

    to_call = {
        False: _need_to_start,
        True: _need_to_continue,
    }

    await to_call[session.in_progress](manager=manager, session_id=session_id)
