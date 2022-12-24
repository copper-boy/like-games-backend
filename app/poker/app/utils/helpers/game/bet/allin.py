from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from orm import PlayerModel


async def do_allin(session: AsyncSession, player: PlayerModel) -> int:
    to_allin = player.game_chips
    await tools.store.game_player_accessor.update_player(
        session=session,
        player_id=player.id,
        values={
            "is_allin": True,
            "game_chips": 0,
            "last_bet": to_allin,
            "round_bet": player.round_bet + to_allin,
        },
    )

    return to_allin
