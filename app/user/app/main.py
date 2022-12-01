from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from sqladmin import Admin
from starlette import status

from api import router as api_router
from core import config, handlers, middlewares, settings, tools
from db.session import _engine
from utils import admin, backend


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/api.user/openapi.json",
        docs_url="/api.user/docs",
        redoc_url="/api.user/redoc",
    )
    application.include_router(api_router, prefix="/api.user")

    def setup_admin() -> Admin:
        authentication_backend = backend.Backend(
            secret_key=config.get_sqladmin_settings().SQLADMIN_SECRET_KEY
        )
        to_return = Admin(
            app=application,
            engine=_engine,
            base_url="/api.user/admin",
            authentication_backend=authentication_backend,
        )
        to_return.add_view(admin.UserModelView)

        return admin

    application.admin = setup_admin()

    @AuthJWT.load_config
    def get_config() -> settings.Settings:
        return settings.Settings()

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
    path="/api.user",
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
