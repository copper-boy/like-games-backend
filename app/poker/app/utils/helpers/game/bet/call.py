from sqlalchemy.ext.asyncio import AsyncSession

from orm import PlayerModel

from .bet import do_bet


async def do_call(session: AsyncSession, player: PlayerModel, last_bet: int) -> int:
    to_call = await do_bet(session=session, player=player, bet=last_bet)

    return to_call
