from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import SessionModel
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
    """
    Creates session in database

    :param api_token:
      admin access token
    :param deck_id:
      deck id in database
    :param game_id:
      game id in database
    :param round_id:
      round id in database
    :param session:
      async database session
    :return:
      created session
    """

    to_select = await tools.store.game_session_accessor.create_session(
        session=session,
        deck_id=deck_id,
        game_id=game_id,
        round_id=round_id,
    )

    return await tools.store.game_session_accessor.get_session_by(
        session=session, where=(SessionModel.id == to_select.id)
    )
