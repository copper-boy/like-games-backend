from __future__ import annotations

from aiohttp import ClientResponseError
from loguru import logger
from sqlalchemy import and_

from core import tools
from db.session import session as sessionmaker
from orm import PlayerModel, SessionModel, UserModel
from schemas import IntegrationPotUpdateSchema
from structures.exceptions import DatabaseError, WSConnectionError, WSStateError


async def new_player(session_id: int, user_id: int, pot: int) -> tuple[int, PlayerModel]:
    async with sessionmaker.begin() as asyncsession:
        session = await tools.store.game_session_accessor.get_session_by(
            session=asyncsession,
            where=(and_(SessionModel.id == session_id, SessionModel.in_progress == False)),
        )
        if not session or session.in_progress:
            raise WSStateError
        if pot < session.game.chips_to_join:
            raise WSConnectionError(f"User {pot=} less than minimal chips to join")

        players = await tools.store.game_player_accessor.get_players_count(
            session=asyncsession, session_id=session.id
        )
        if players == session.game.max_players:
            raise DatabaseError

        user = await tools.store.game_user_accessor.get_user_by(
            session=asyncsession, where=(UserModel.id == user_id)
        )
        to_select = await tools.store.game_player_accessor.create_player(
            session=asyncsession,
            game_chips=session.game.chips_to_join,
            user_id=user.id,
            session_id=session.id,
        )
        player = await tools.store.game_player_accessor.get_player_by(
            session=asyncsession, where=(PlayerModel.id == to_select.id)
        )

    new_balance = pot - session.game.chips_to_join
    return new_balance, player


async def delete_player(player: PlayerModel, user_id: int, preview_balance: int) -> None:
    to_update = IntegrationPotUpdateSchema(pot=player.game_chips + preview_balance)

    try:
        await tools.store.integration_pot_accessor.update_pot(user_id=user_id, json=to_update)
    except ClientResponseError as e:
        logger.exception(e)

    async with sessionmaker.begin() as asyncsession:
        await tools.store.game_player_accessor.delete_player(
            session=asyncsession, player_id=player.id
        )
