from fastapi import FastAPI
from starlette import status
from starlette.responses import HTMLResponse

from api import router as api_router
from core import middlewares, tools
from handlers import setup_handlers


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/api.poker/openapi.json",
        docs_url="/api.poker/docs",
        redoc_url="/api.poker/redoc",
    )
    application.include_router(api_router)

    @application.on_event(event_type="startup")
    async def startup() -> None:
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
