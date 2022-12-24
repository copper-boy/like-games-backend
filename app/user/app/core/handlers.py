from __future__ import annotations

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from loguru import logger


def __bad_response(status_code: int, detail: dict) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail},
    )


def register_authjwtexception_handler(app: FastAPI) -> None:
    @app.exception_handler(AuthJWTException)
    async def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:
        logger.info(
            "With request=([%s][%s][%s]) occurred error=([%s][%s])",
            request.method,
            request.url,
            request.query_params,
            exc.status_code,
            exc.message,
        )
        return __bad_response(status_code=exc.status_code, detail=exc.message)


def register_httpexception_handler(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        logger.info(
            "With request=([%s][%s][%s]) occurred error=([%s][%s])",
            request.method,
            request.url,
            request.query_params,
            exc.status_code,
            exc.detail,
        )
        return __bad_response(status_code=exc.status_code, detail=exc.detail)


def register_all_exception_handlers(app: FastAPI) -> None:
    register_authjwtexception_handler(app)
    register_httpexception_handler(app)
