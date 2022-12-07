from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from schemas import SessionSchema
from utils import decorators

router = APIRouter()


@router.post(
    path="/create/session",
    response_model=SessionSchema,
    status_code=status.HTTP_201_CREATED,
)
@decorators.admin_required(target="api_token")
async def create_session(
    api_token: str = Query(...),
    deck_id: int = Query(...),
    game_id: int = Query(...),
    round_id: int = Query(...),
    session: AsyncSession = Depends(depends.get_session),
) -> SessionSchema:
    async with session.begin_nested() as nested_session:
        to_return = await tools.store.game_session_accessor.create_session(
            session=nested_session.session,
            deck_id=deck_id,
            game_id=game_id,
            round_id=round_id,
        )

    return to_return
