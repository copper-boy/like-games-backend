from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import GameModel, RoundModel
from schemas import SessionSchema
from utils import decorators

router = APIRouter()


@router.post(
    path="/create/game",
    response_model=SessionSchema,
    status_code=status.HTTP_201_CREATED,
)
@decorators.admin_required(target="api_token")
async def create_session(
    api_token: str = Query(...),
    game_id: int = Query(...),
    round_id: int = Query(...),
    session: AsyncSession = Depends(depends.get_session),
) -> SessionSchema:
    game = await tools.store.game_accessor.get_game_by(
        session=session, where=(GameModel.id == game_id)
    )
    round = await tools.store.game_round_accessor.get_round_by(
        session=session, where=(RoundModel.id == round_id)
    )

    async with session.begin_nested() as nested_session:
        to_return = await tools.store.game_session_accessor.create_session(
            session=nested_session.session,
            game=game,
            round=round,
        )

    return to_return
