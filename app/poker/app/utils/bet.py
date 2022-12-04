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


async def do_call(session: AsyncSession, player: PlayerModel, last_bet: int) -> int:
    to_call = await do_bet(session=session, player=player, bet=last_bet)

    return to_call


async def do_check() -> int:
    to_check = 0

    return to_check


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


async def do_up(session: AsyncSession, player: PlayerModel, bet: int) -> int:
    to_up = await do_bet(session=session, player=player, bet=bet)

    return to_up
