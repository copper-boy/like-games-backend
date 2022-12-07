from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from structures.enums import PlayerActionEnum


async def release_action(
    session: AsyncSession,
    session_id: int,
    round_bet: int,
    max_bet: int,
    pot: int,
    player_id: int,
    bet: int,
    action: PlayerActionEnum,
) -> None:
    await tools.store.game_session_accessor.update_session(
        session=session,
        session_id=session_id,
        values={
            "last_player": player_id,
            "last_player_action": action,
            "max_bet": round_bet if round_bet > max_bet else max_bet,
            "pot": pot + bet,
        },
    )
    await tools.store.game_session_accessor.set_next_player(session=session, session_id=session_id)
