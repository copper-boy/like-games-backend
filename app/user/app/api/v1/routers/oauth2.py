from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends
from orm import UserModel
from schemas import UserSchema
from utils import auth, token, user

router = APIRouter()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api.user.oauth2.login")


@router.post(
    path="/oauth2/login",
    response_description="The access token",
    status_code=status.HTTP_200_OK,
)
async def login(
    authorize: AuthJWT = Depends(),
    oauth_form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(depends.get_session),
) -> UserSchema:
    authed_user = await auth.authenticate_user(
        session=session, email=oauth_form.username, password=oauth_form.password
    )
    if not authed_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="incorrect login data posted"
        )
    access_token = token.create_access_token(authorize=authorize, subject=authed_user.id)

    return {"access_token": access_token, "token_type": "bearer"}


async def get_user(
    authorize: AuthJWT = Depends(),
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(depends.get_session),
) -> UserModel:
    current_user = await user.get_user_by_raw_token(
        authorize=authorize, raw_token=token, session=session
    )

    return current_user


@router.get(
    path="/oauth2/current",
    response_description="The current user who called this method",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def current(current_user: UserSchema = Depends(get_user)) -> UserSchema:
    return current_user
