from __future__ import annotations

from fastapi import FastAPI
from starlette import status
from starlette.responses import HTMLResponse

from api import router as api_router
from core import middlewares, tools
from misc import sch


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/api.poker/openapi.json",
        docs_url="/api.poker/docs",
        redoc_url="/api.poker/redoc",
    )
    application.include_router(api_router, prefix="/api.poker")

    @application.on_event(event_type="startup")
    async def startup() -> None:
        await tools.store.connect()
        sch.start()

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
    path="/api.poker/home",
    status_code=status.HTTP_200_OK,
)
async def home() -> HTMLResponse:
    with open("home.html", "r") as file:
        html = file.read()

    return HTMLResponse(html)
