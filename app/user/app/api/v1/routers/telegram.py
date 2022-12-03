from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.requests import Request
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends
from schemas import UserSchema
from utils import helpers, telegram, token

router = APIRouter()


@router.post(
    path="/telegram/link",
    response_description="The user on successful login",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def link(
    request: Request,
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(depends.get_session),
) -> UserSchema:
    exists = helpers.optional_user(authorize=authorize, session=session)

    try:
        request_data = telegram.verify_telegram_authentication(query=request.query_params)
    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="can't verify data")

    if not exists:
        user = await helpers.create_new_user_telegram(
            session=session,
            telegram=request_data.id,
            username=request_data.username,
        )

        token.create_token_and_set_to_cookies(authorize=authorize, subject=user.id)
    else:
        user = exists

        await helpers.link_to_exists(session=session, user_id=user.id, telegram=request_data.id)

    return user
