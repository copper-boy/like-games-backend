from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import GameModel
from schemas import GameSchema

router = APIRouter()


@router.post(
    path="/view/game/{game_id}",
    response_model=GameSchema,
    status_code=status.HTTP_200_OK,
)
async def view_game(
    game_id: int = Query(...), session: AsyncSession = Depends(depends.get_session)
) -> GameSchema:
    async with session.begin_nested() as nested_session:
        to_return = await tools.store.game_accessor.get_game_by(
            session=nested_session.session, where=(GameModel.id == game_id)
        )

    return to_return
