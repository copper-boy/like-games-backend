from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from utils import helpers


async def _set_blind(session: AsyncSession, to_player: int, blind: int) -> int:
    player_blind = await helpers.get_player_by_id(session=session, player_id=to_player)
    last_blind_bet = player_blind.game_chips if to_player >= player_blind.game_chips else blind

    await tools.store.game_player_accessor.update_player(
        session=session,
        player_id=player_blind.id,
        values={
            "last_bet": last_blind_bet,
            "round_bet": player_blind.round_bet + last_blind_bet,
            "game_chips": player_blind.game_chips - last_blind_bet,
        },
    )

    return last_blind_bet


async def set_blinds(
    session: AsyncSession,
    session_id: int,
) -> tuple[int, int]:
    s = await helpers.get_session_with_raise(session=session, session_id=session_id)

    last_small_blind_bet = await _set_blind(
        session=session,
        to_player=s.small_blind_position,
        blind=s.game.small_blind,
    )
    last_big_blind_bet = await _set_blind(
        session=session,
        to_player=s.big_blind_position,
        blind=s.game.big_blind,
    )

    await tools.store.game_session_accessor.update_session(
        session=session,
        session_id=session_id,
        values={"pot": s.pot + last_small_blind_bet + last_big_blind_bet},
    )

    return last_small_blind_bet, last_big_blind_bet
