from fastapi import APIRouter
from fastapi.param_functions import Body, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from schemas import GameSchema
from utils import decorators

router = APIRouter()


@router.post(
    path="/create/game",
    response_model=GameSchema,
    status_code=status.HTTP_201_CREATED,
)
@decorators.admin_required(target="api_token")
async def create_game(
    api_token: str = Query(...),
    min_players: int = Body(default=2),
    max_players: int = Body(default=9),
    chips_to_join: int = Body(default=10000),
    small_blind: int = Body(default=50),
    big_blind: int = Body(default=100),
    session: AsyncSession = Depends(depends.get_session),
) -> GameSchema:
    """
    Creates the game in database

    :param api_token:
      admin access token
    :param min_players:
      min numbers of players in game
    :param max_players:
      max numbers of players in game
    :param chips_to_join:
      min chips to join in the game
    :param small_blind:
      small blind bet
    :param big_blind:
      big blind bet
    :param session:
      async database session
    :return:
      created game
    """

    async with session.begin_nested() as nested_session:
        to_return = await tools.store.game_accessor.create_game(
            min_players=min_players,
            max_players=max_players,
            chips_to_join=chips_to_join,
            small_blind=small_blind,
            big_blind=big_blind,
            session=nested_session.session,
        )

    return to_return
