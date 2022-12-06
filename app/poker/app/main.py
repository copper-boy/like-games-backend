from fastapi import FastAPI
from starlette import status
from starlette.responses import HTMLResponse

import handlers  # noqa
from api import router as api_router
from core import middlewares, tools


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
    return HTMLResponse(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<button onclick="sendMessage(event)">Send</button>

<script>
    let ws = new WebSocket("ws://localhost/api.poker/ws/1");

    ws.onopen = (event) => {
        console.log("connected");
    };
    ws.onmessage = (event) => {
        console.log(event.data.length);
    }

    function sendMessage(event) {
        const msg = {
            event: "helper",
            payload: {
                "to_filter": "commands",
            }
        };

        ws.send(JSON.stringify(msg));

        event.preventDefault();
    }
</script>
</body>
</html>
"""
    )
