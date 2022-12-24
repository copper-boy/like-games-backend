from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from orm import PlayerModel


async def do_fold(session: AsyncSession, player: PlayerModel) -> int:
    to_fold = 0
    await tools.store.game_player_accessor.update_player(
        session=session,
        player_id=player.id,
        values={
            "is_folded": True,
        },
    )

    return to_fold
