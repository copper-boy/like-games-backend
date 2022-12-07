from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from orm import PlayerModel


async def do_bet(session: AsyncSession, player: PlayerModel, bet: int) -> int:
    to_bet = bet
    await tools.store.game_player_accessor.update_player(
        session=session,
        player_id=player.id,
        values={
            "game_chips": player.game_chips - to_bet,
            "last_bet": to_bet,
            "round_bet": player.round_bet + to_bet,
        },
    )

    return to_bet
