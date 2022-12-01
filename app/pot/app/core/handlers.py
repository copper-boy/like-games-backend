from aiohttp.client_exceptions import ClientResponseError
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from loguru import logger


def __bad_response(status_code: int, detail: dict) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail},
    )


def register_clientresponseerror_handler(app: FastAPI) -> None:
    @app.exception_handler(ClientResponseError)
    async def clientresponseerror_handler(
        request: Request, exc: ClientResponseError
    ) -> JSONResponse:
        logger.info(
            "With request=([%s][%s][%s]) occurred error=([%s][%s])",
            request.method,
            request.url,
            request.query_params,
            exc.status,
            exc.message,
        )

        return __bad_response(
            status_code=exc.status,
            detail=exc.message,
        )


def register_httpexception_handler(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def httpexception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        logger.info(
            "With request=([%s][%s][%s]) occurred error=([%s][%s])",
            request.method,
            request.url,
            request.query_params,
            exc.status_code,
            exc.detail,
        )

        return __bad_response(
            status_code=exc.status_code,
            detail=exc.detail,
        )


def register_all_exception_handlers(app: FastAPI) -> None:
    register_clientresponseerror_handler(app)
    register_httpexception_handler(app)
