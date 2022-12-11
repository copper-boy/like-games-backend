from fastapi import FastAPI
from starlette import status

from api import router as api_router
from core import handlers, middlewares, tools


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/api.pot/openapi.json",
        docs_url="/api.pot/docs",
        redoc_url="/api.pot/redoc",
    )
    application.include_router(api_router, prefix="/api.pot")

    @application.on_event(event_type="startup")
    async def startup() -> None:
        await tools.store.connect()

    @application.on_event(event_type="shutdown")
    async def shutdown() -> None:
        await tools.store.disconnect()

    handlers.register_all_exception_handlers(app=application)
    middlewares.register_middlewares(app=application)

    return application


app = create_application()


@app.get(
    path="/api.pot",
    status_code=status.HTTP_200_OK,
)
async def root() -> dict:
    return {
        "service": {
            "status": "Okay",
            "health": "Okay",
            "production_ready": True,
        }
    }
