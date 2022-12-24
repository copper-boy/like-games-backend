from __future__ import annotations

from asyncio import sleep
from typing import TYPE_CHECKING

from core import tools
from db.session import session as sessionmaker
from schemas import EventSchema
from utils import helpers

if TYPE_CHECKING:
    from ws import WSManager


async def start_session_task(manager: WSManager, session_id: int) -> None:
    await manager.broadcast_json(
        event=EventSchema(
            path="serverStartGame",
            payload={
                "data": {
                    "start_after": 15,
                },
            },
        )
    )

    await sleep(15)

    async with sessionmaker.begin() as session:
        await tools.store.game_session_accessor.update_session(
            session=session,
            session_id=session_id,
            values={
                "in_progress": True,
            },
        )
        async with session.begin_nested() as nested_session:
            await helpers.set_players_in_session(
                session=nested_session.session, session_id=session_id
            )
        await helpers.set_blinds(
            session=session,
            session_id=session_id,
        )

    await manager.broadcast_json(
        event=EventSchema(
            path="serverGameStarted",
        )
    )
