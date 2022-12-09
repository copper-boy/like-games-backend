from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from orm import PlayerModel


async def is_all_allin(session: AsyncSession, session_id: int) -> bool:
    players = await tools.store.game_player_accessor.get_players_by(
        session=session, where=(PlayerModel.session_id == session_id)
    )
    players_count = await tools.store.game_player_accessor.get_players_count(
        session=session, session_id=session_id
    )

    allin_count = 0
    fold_count = 0
    for player in players:
        if player.is_allin:
            allin_count += 1
        if player.is_folded:
            fold_count += 1

    return players_count == (allin_count + fold_count)
