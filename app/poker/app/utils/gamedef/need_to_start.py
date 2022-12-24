from __future__ import annotations

from asyncio import create_task
from typing import TYPE_CHECKING

from core import tools
from db.session import session as sessionmaker
from orm import SessionModel

if TYPE_CHECKING:
    from ws import WSManager

from .tasks import start_session_task


async def need_to_start(manager: WSManager, session_id: int) -> None:
    async with sessionmaker.begin() as asyncsession:
        session = await tools.store.game_session_accessor.get_session_by(
            session=asyncsession, where=(SessionModel.id == session_id)
        )
        players = await tools.store.game_player_accessor.get_players_count(
            session=asyncsession, session_id=session.id
        )

    if players >= session.game.min_players:
        if players != manager.last_known_connected:
            if manager.start_session_task:
                manager.start_session_task.cancel()

            manager.last_known_connected = players
            manager.start_session_task = create_task(
                start_session_task(manager=manager, session_id=session_id)
            )
    else:
        if manager.start_session_task:
            manager.start_session_task.cancel()
