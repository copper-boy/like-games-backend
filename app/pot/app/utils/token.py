from fastapi_jwt_auth import AuthJWT


def create_token(authorize: AuthJWT, subject: str | int) -> tuple[str, str]:
    access_token = authorize.create_access_token(subject=subject)
    refresh_token = authorize.create_refresh_token(subject=subject)

    return access_token, refresh_token
