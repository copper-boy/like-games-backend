from typing import Any, Callable

from fastapi import FastAPI
from fastapi.requests import Request

from db.session import session


async def session_http_middleware(request: Request, call_next: Callable) -> Any:
    async with session.begin() as s:
        request.state.session = s

        response = await call_next(request)

    return response


def register_http_middlewares(app: FastAPI) -> None:
    app.middleware("http")(session_http_middleware)


def register_middlewares(app: FastAPI) -> None:
    register_http_middlewares(app=app)
