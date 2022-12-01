from fastapi import FastAPI
from starlette import status

from core import middlewares, tools
from db.base import Base
from db.session import _engine, session
from orm import *
from schemas import GameSchema, RoundSchema, SessionSchema


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/api.poker/openapi.json",
        docs_url="/api.poker/docs",
        redoc_url="/api.poker/redoc",
    )

    @application.on_event(event_type="startup")
    async def startup() -> None:
        async with _engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        await tools.store.connect()

    @application.on_event(event_type="shutdown")
    async def shutdown() -> None:
        await tools.store.disconnect()

    middlewares.register_middlewares(app=application)

    return application


app = create_application()


@app.get(
    path="/api.poker",
    status_code=status.HTTP_200_OK,
)
async def root() -> dict:
    return {"service": {"status": "Bad", "health": "Okay", "production_ready": False}}


@app.get(
    path="/api.poker.create.game",
    status_code=status.HTTP_200_OK,
    response_model=GameSchema,
)
async def create_game() -> GameSchema:
    async with session.begin() as s:
        game = await store.game_accessor.create_game(session=s)

    return game


@app.get(
    path="/api.poker.create.round",
    status_code=status.HTTP_200_OK,
    response_model=RoundSchema,
)
async def create_round() -> RoundSchema:
    async with session.begin() as s:
        round = await store.game_round_accessor.create_round(session=s)

    return round


@app.get(
    path="/api.poker.create.session",
    status_code=status.HTTP_200_OK,
    response_model=SessionSchema,
)
async def create_session():
    async with session.begin() as s:
        game = await store.game_accessor.get_game_by(session=s, where=(GameModel.id == 1))
        round = await store.game_round_accessor.get_round_by(session=s, where=(RoundModel.id == 1))
        _session = await store.game_session_accessor.create_session(
            session=s, game=game, round=round
        )

    return _session


@app.get(
    path="/api.poker.session.filter",
    status_code=status.HTTP_200_OK,
)
async def filter_sessions(
    offset: int,
    limit: int,
) -> list[SessionSchema]:
    async with session.begin() as s:
        result = await store.game_session_accessor.filter_sessions(
            session=s, offset=offset, limit=limit
        )

    return result
