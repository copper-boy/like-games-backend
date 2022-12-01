from fastapi import APIRouter
from fastapi.param_functions import Body, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from schemas import SessionSchema
from structures.enums import GameTypeEnum

router = APIRouter()


@router.get(
    path="/filter/sessions/count",
    status_code=status.HTTP_200_OK,
    response_model=list[SessionSchema],
)
async def filter_sessions(
    session: AsyncSession = Depends(depends.get_session),
    type: GameTypeEnum = Body(default=GameTypeEnum.texas),
    max_players: int = Body(default=9),
    small_blind: int = Body(default=50),
    chips_to_join: int = Body(default=10000),
) -> list[SessionSchema]:
    to_return = await tools.store.game_session_accessor.get_filter_count(
        session=session,
        type=type,
        max_players=max_players,
        small_blind=small_blind,
        chips_to_join=chips_to_join,
    )

    return to_return


@router.get(
    path="/filter/sessions",
    status_code=status.HTTP_200_OK,
    response_model=list[SessionSchema],
)
async def filter_sessions(
    session: AsyncSession = Depends(depends.get_session),
    offset: int = Query(default=0, le=100),
    limit: int = Query(default=100, le=100),
    type: GameTypeEnum = Body(default=GameTypeEnum.texas),
    max_players: int = Body(default=9),
    small_blind: int = Body(default=50),
    chips_to_join: int = Body(default=10000),
) -> list[SessionSchema]:
    to_return = await tools.store.game_session_accessor.filter_sessions(
        session=session,
        offset=offset,
        limit=limit,
        type=type,
        max_players=max_players,
        small_blind=small_blind,
        chips_to_join=chips_to_join,
    )

    return to_return
