from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import RoundModel
from schemas import RoundSchema
from utils import decorators

router = APIRouter()


@router.post(
    path="/create/round",
    response_model=RoundSchema,
    status_code=status.HTTP_201_CREATED,
)
@decorators.admin_required(target="api_token")
async def create_round(
    api_token: str = Query(...), session: AsyncSession = Depends(depends.get_session)
) -> RoundSchema:
    """
    Creates the round in database

    :param api_token:
      admin access token
    :param session:
      async database session
    :return:
      created round
    """

    to_select = await tools.store.game_round_accessor.create_round(session=session)

    return await tools.store.game_round_accessor.get_round_by(
        session=session, where=(RoundModel.id == to_select.id)
    )
