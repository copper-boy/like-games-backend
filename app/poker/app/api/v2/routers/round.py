from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import RoundModel
from schemas import RoundSchema

router = APIRouter()


@router.get(
    path="/view/round/{round_id}",
    response_model=RoundSchema,
    status_code=status.HTTP_200_OK,
)
async def view_round(
    round_id: int = Query(...), session: AsyncSession = Depends(depends.get_session)
) -> RoundSchema:
    """
    Returns the round
    :param round_id:
      round id in database
    :param session:
      async database session
    :return:
      round from database
    """
    async with session.begin_nested() as nested_session:
        to_return = await tools.store.game_round_accessor.get_round_by(
            session=nested_session.session, where=(RoundModel.id == round_id)
        )

    return to_return
