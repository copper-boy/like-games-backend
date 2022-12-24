from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from db.session import session as sessionmaker
from orm import SessionModel
from utils import gamedef, helpers

if TYPE_CHECKING:
    from ws import WSManager

from .check import check_player


async def __not_allin(
    asyncsession: AsyncSession, session: SessionModel, manager: WSManager
) -> None:
    async with asyncsession.begin_nested() as nested_asyncsession:
        await check_player(
            session=nested_asyncsession.session,
            manager=manager,
            session_id=session.id,
            player_id=session.current_player,
        )
    await gamedef.handlers.round_type(
        session=asyncsession,
        current_player=session.current_player,
        max_bet=session.max_bet,
        manager=manager,
    )


async def __allin(asyncsession: AsyncSession, session: SessionModel) -> None:
    await helpers.next_round_call(asyncsession=asyncsession, session_id=session.id)


async def need_to_continue(manager: WSManager, session_id: int) -> None:
    async with sessionmaker.begin() as asyncsession:
        session = await helpers.get_session_with_raise(session=asyncsession, session_id=session_id)
        if not await helpers.is_all_allin(session=asyncsession, session_id=session_id):
            await __not_allin(asyncsession=asyncsession, session=session, manager=manager)
        else:
            await __allin(asyncsession=asyncsession, session=session)
