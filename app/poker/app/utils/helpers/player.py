from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from orm import PlayerModel


async def get_player(session: AsyncSession, user_id: int) -> PlayerModel:
    player = await tools.store.game_player_accessor.get_player_by(
        session=session, where=(PlayerModel.user_id == user_id)
    )

    return player


async def get_player_by_id(session: AsyncSession, player_id: int) -> PlayerModel:
    player = await tools.store.game_player_accessor.get_player_by(
        session=session, where=(PlayerModel.id == player_id)
    )

    return player


async def get_player_with_last_player(
    session: AsyncSession, player_id: int, last_player: int
) -> tuple[PlayerModel, PlayerModel]:
    player = await get_player_by_id(session=session, player_id=player_id)
    last_player = await get_player_by_id(session=session, player_id=last_player)

    return player, last_player
