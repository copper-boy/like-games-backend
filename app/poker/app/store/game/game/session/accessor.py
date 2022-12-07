from typing import Any

from sqlalchemy import and_, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import GameModel, PlayerModel, SessionModel
from store.base import BaseAccessor
from structures.exceptions import DatabaseAccessorError


class SessionAccessor(BaseAccessor):
    async def create_session(
        self,
        session: AsyncSession,
        deck_id: int,
        game_id: int,
        round_id: int,
    ) -> SessionModel:
        is_deck_have_session = await self.store.deck_accessor.is_already_taken(
            session=session, deck_id=deck_id
        )
        is_round_have_session = await self.store.game_round_accessor.is_already_taken(
            session=session, round_id=round_id
        )
        if is_deck_have_session or is_round_have_session:
            raise DatabaseAccessorError

        to_return = SessionModel(deck_id=deck_id, game_id=game_id, round_id=round_id)

        session.add(to_return)

        return to_return

    async def update_session(self, session: AsyncSession, session_id: int, values: dict) -> None:
        await session.execute(
            update(SessionModel).where(SessionModel.id == session_id).values(**values)
        )

    async def get_session_by(self, session: AsyncSession, where: Any) -> SessionModel:
        to_return = await session.execute(
            select(SessionModel)
            .where(where)
            .options(joinedload(SessionModel.game))
            .options(joinedload(SessionModel.round))
        )

        return to_return.scalar()

    async def set_next_player(self, session: AsyncSession, session_id: int) -> None:
        s = await self.get_session_by(session=session, where=(SessionModel.id == session_id))
        players = await self.store.game_player_accessor.get_players_by(
            session=s, where=(PlayerModel.session_id == s.id)
        )

        for index, player in enumerate(players, start=0):
            if player.id == s.current_player:
                try:
                    to_set = players[index + 1].id
                except IndexError:
                    to_set = players[0].id
                finally:
                    break
        await self.update_session(
            session=session, session_id=s.id, values={"current_player": to_set}  # noqa
        )

    async def players(self, session: AsyncSession, s: SessionModel, new: int) -> None:
        await self.update_session(
            session=session,
            session_id=s.id,
            values={"players_connected": s.players_connected + new},
        )

    async def filter_sessions(  # noqa
        self,
        session: AsyncSession,
        offset: int,
        limit: int,
        max_players: int = 9,
        small_blind: int = 50,
        chips_to_join: int = 10000,
    ) -> list[SessionModel]:
        to_return = await session.execute(
            select(SessionModel)
            .filter(
                (GameModel.max_players == max_players)
                & (GameModel.small_blind == small_blind)
                & (GameModel.chips_to_join == chips_to_join)
            )
            .where(
                and_(
                    SessionModel.players_connected < GameModel.max_players,
                    SessionModel.in_progress == False,
                )
            )
            .join(GameModel)
            .order_by(desc(SessionModel.players_connected))
            .offset(offset)
            .limit(limit)
        )

        return to_return.scalars().all()

    async def get_filter_count(
        self,
        session: AsyncSession,
        max_players: int = 9,
        small_blind: int = 50,
        chips_to_join: int = 10000,
    ) -> int:
        to_return = await session.execute(
            select(func.count(SessionModel.id))
            .filter(
                (GameModel.max_players == max_players)
                & (GameModel.small_blind == small_blind)
                & (GameModel.chips_to_join == chips_to_join)
            )
            .where(
                and_(
                    SessionModel.players_connected < GameModel.max_players,
                    SessionModel.in_progress == False,
                )
            )
            .join(GameModel)
            .select_from(SessionModel)
        )

        return to_return.scalar()
