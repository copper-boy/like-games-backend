from sqlalchemy.ext.asyncio import AsyncSession

from core import tools
from orm import CardModel, PlayerModel, SessionModel, UserModel
from orm.player import user
from schemas import CardSchema, PlayerSchema
from structures.exceptions import WSStateError


async def create_player(session: AsyncSession, session_id: int, user_id: int) -> PlayerModel:
    assign_to = await tools.store.game_session_accessor.get_session_by(
        session=session, where=(SessionModel.id == session_id)
    )
    user = await tools.store.game_user_accessor.get_user_by(
        session=session, where=(UserModel.user_id == user_id)
    )
    player = await tools.store.game_player_accessor.create_player(
        session=session, user=user, assign_to=assign_to
    )

    return player


async def delete_player(session: AsyncSession, user_id: int) -> None:
    try:
        player = await get_player(session=session, user_id=user_id)
    except WSStateError:
        return None

    await tools.store.game_player_accessor.delete_player(session=session, player_id=player.id)


async def get_player(session: AsyncSession, user_id: int) -> PlayerModel:
    user = await tools.store.game_user_accessor.get_user_by(
        session=session, where=(UserModel.user_id == user_id)
    )
    player = await tools.store.game_player_accessor.get_player_by(
        session=session, where=(PlayerModel.user_id == user.id)
    )
    if not player:
        raise WSStateError

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
    last_player = await tools.store.game_player_accessor.get_player_by(
        session=session, where=(PlayerModel.id == last_player)
    )

    return player, last_player


async def get_session_with_raise(session: AsyncSession, session_id: int) -> SessionModel:
    s = await tools.store.game_session_accessor.get_session_by(
        session=session, where=(SessionModel.id == session_id)
    )
    if not s.in_progress:
        raise WSStateError

    return s


def cards_to_pydantic(cards: list[CardModel]) -> list[CardSchema]:
    to_return: list[CardSchema] = []
    for card in cards:
        to_return.append(CardSchema.from_orm(card))

    return to_return


def players_to_pydantic(players: list[PlayerModel], exclude: int) -> list[PlayerSchema]:
    to_return: list[PlayerSchema] = []
    for player in players:
        if player.id == exclude:
            continue
        to_return.append(PlayerSchema.from_orm(player))

    return to_return
