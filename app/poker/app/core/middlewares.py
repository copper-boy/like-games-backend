from typing import Any, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request

from db.session import session


async def session_http_middleware(request: Request, call_next: Callable) -> Any:
    async with session.begin() as s:
        request.state.session = s

        response = await call_next(request)

    return response


def cors_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_http_middlewares(app: FastAPI) -> None:
    app.middleware("http")(session_http_middleware)
    cors_middleware(app=app)


def register_middlewares(app: FastAPI) -> None:
    register_http_middlewares(app=app)
