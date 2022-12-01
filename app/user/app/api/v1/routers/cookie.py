from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends
from schemas import UserLoginSchema, UserSchema
from utils import auth, decorators, token, user

router = APIRouter()


@router.post(
    path="/cookie/login",
    response_description="The user on successful login",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    user_data: UserLoginSchema,
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(depends.get_session),
) -> UserSchema:
    authed_user = await auth.authenticate_user(
        session=session, email=user_data.email, password=user_data.password
    )
    if not authed_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="incorrect login data posted"
        )
    token.create_token_and_set_to_cookies(authorize=authorize, subject=authed_user.id)

    return authed_user


@router.delete(
    path="/cookie/logout",
    response_model=UserSchema,
    response_description="A user who has logged out",
    status_code=status.HTTP_200_OK,
)
@decorators.login_required(target="authorize", attribute="jwt_required")
async def logout(
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(depends.get_session),
) -> UserSchema:
    current_user = await user.get_user(authorize=authorize, session=session)

    token.unset_cookies_token(authorize=authorize)

    return current_user


@router.post(
    path="/cookie/refresh",
    response_description="The user",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
@decorators.login_required(target="authorize", attribute="jwt_refresh_token_required")
async def refresh(
    authorize: AuthJWT = Depends(), session: AsyncSession = Depends(depends.get_session)
) -> UserSchema:
    current_user = await user.get_user(authorize=authorize, session=session)

    token.refresh_and_set_access_token(authorize=authorize)

    return current_user


@router.get(
    path="/cookie/current",
    response_description="The current user who called this method",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
@decorators.login_required(target="authorize", attribute="jwt_required")
async def current(
    authorize: AuthJWT = Depends(), session: AsyncSession = Depends(depends.get_session)
) -> UserSchema:
    current_user = await user.get_user(authorize=authorize, session=session)

    return current_user
