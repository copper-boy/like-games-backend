from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from orm import PlayerModel, SessionModel
from structures.exceptions.ws.errors import WSStateError


async def get_session_with_raise(session: AsyncSession, session_id: int) -> SessionModel:
    s = await tools.store.game_session_accessor.get_session_by(
        session=session, where=(SessionModel.id == session_id)
    )
    if not s.in_progress:
        raise WSStateError

    return s


async def _two_players(session: AsyncSession, session_id: int, players: list[PlayerModel]) -> None:
    await tools.store.game_session_accessor.update_session(
        session=session,
        session_id=session_id,
        values={
            "current_player": players[0].id,
            "small_blind_position": players[0].id,
            "big_blind_position": players[1].id,
        },
    )


async def _gt_two_players(
    session: AsyncSession, session_id: int, players: list[PlayerModel]
) -> None:
    await tools.store.game_session_accessor.update_session(
        session=session,
        session_id=session_id,
        values={
            "current_player": players[-1].id,
            "small_blind_position": players[0].id,
            "big_blind_position": players[1].id,
        },
    )


async def set_players_in_session(session: AsyncSession, session_id: int) -> None:
    s = await get_session_with_raise(session=session, session_id=session_id)

    players = await tools.store.game_player_accessor.get_players_by_order_in_game_order(
        session=session, session_id=s.id
    )
    players_connected = await tools.store.game_player_accessor.get_players_count(
        session=session, session_id=s.id
    )

    to_update = {
        2: _two_players,
    }
    to_call = to_update.get(players_connected, _gt_two_players)
    await to_call(session=session, session_id=s.id, players=players)
