from typing import Any

from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import GameModel, PlayerModel, RoundModel, SessionModel, UserModel
from store.base import BaseAccessor
from structures.enums import GameTypeEnum
from structures.exceptions import DatabaseAccessorError


class SessionAccessor(BaseAccessor):
    async def create_session(
        self,
        session: AsyncSession,
        game: GameModel,
        round: RoundModel,
    ) -> SessionModel:
        is_round_have_session = await self.store.game_round_accessor.is_already_taken(
            session=session, round_id=round.id
        )
        if is_round_have_session:
            raise DatabaseAccessorError

        to_return = SessionModel(game=game, round=round)

        session.add(to_return)

        return to_return

    async def get_session_by(self, session: AsyncSession, where: Any) -> SessionModel:
        to_return = await session.execute(select(SessionModel).where(where))

        return to_return.scalar()

    async def add_player(
        self, session: AsyncSession, session_id: int, user_id: int
    ) -> SessionModel:
        assign_to = await self.get_session_by(
            session=session, where=(SessionModel.id == session_id)
        )
        user = await self.store.game_user_accessor.get_user_by(
            session=session, where=(UserModel.id == user_id)
        )
        self.store.game_player_accessor.create_player(
            session=session, user=user, assign_to=assign_to
        )

        return assign_to

    async def remove_player(self, session: AsyncSession, player_id: int) -> SessionModel:
        assigned_to = await session.execute(
            select(SessionModel).where(PlayerModel.id == player_id).join(PlayerModel)
        )

        await self.store.game_player_accessor.delete_player(session=session, player_id=player_id)

        return assigned_to

    async def filter_sessions(
        self,
        session: AsyncSession,
        offset: int,
        limit: int,
        type: GameTypeEnum = GameTypeEnum.texas,
        max_players: int = 9,
        small_blind: int = 50,
        chips_to_join: int = 10000,
    ) -> list[SessionModel]:
        to_return = await session.execute(
            select(SessionModel)
            .filter(
                (GameModel.type == type)
                & (GameModel.max_players == max_players)
                & (GameModel.small_blind == small_blind)
                & (GameModel.chips_to_join == chips_to_join)
            )
            .where(
                and_(
                    SessionModel.players_connected < GameModel.max_players,
                    SessionModel.in_progress == False,
                )
            )
            .options(joinedload(SessionModel.game))
            .options(joinedload(SessionModel.round))
            .join(GameModel)
            .order_by(desc(SessionModel.players_connected))
            .offset(offset)
            .limit(limit)
        )

        return to_return.scalars().all()

    async def get_filter_count(
        self,
        session: AsyncSession,
        type: GameTypeEnum = GameTypeEnum.texas,
        max_players: int = 9,
        small_blind: int = 50,
        chips_to_join: int = 10000,
    ) -> int:
        to_return = await session.execute(
            select(func.count(SessionModel.id))
            .filter(
                (GameModel.type == type)
                & (GameModel.max_players == max_players)
                & (GameModel.small_blind == small_blind)
                & (GameModel.chips_to_join == chips_to_join)
            )
            .where(SessionModel.players_connected < GameModel.max_players)
            .join(GameModel)
            .select_from(SessionModel)
        )

        return to_return.scalar()
