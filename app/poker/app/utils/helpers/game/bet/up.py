from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from orm import PlayerModel

from .bet import do_bet


async def do_up(session: AsyncSession, player: PlayerModel, bet: int) -> int:
    to_up = await do_bet(session=session, player=player, bet=bet)

    return to_up
