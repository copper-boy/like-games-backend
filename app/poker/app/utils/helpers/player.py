from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from orm import PlayerModel
from utils import helpers

if TYPE_CHECKING:
    from ws import WSManager


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


async def delete_players_with_zero_balance(
    session: AsyncSession, session_id: int, manager: WSManager
) -> None:
    players = await tools.store.game_player_accessor.get_players_by(
        session=session,
        where=and_(PlayerModel.session_id == session_id, PlayerModel.game_chips == 0),
    )
    for player in players:
        await helpers.delete_player(manager=manager, player_id=player.id, preview_balance=0)
