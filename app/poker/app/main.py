from fastapi import FastAPI
from starlette import status
from starlette.responses import HTMLResponse

import handlers  # noqa
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
        from db.base import Base
        from db.session import _engine

        async with _engine.begin() as s:
            await s.run_sync(Base.metadata.drop_all)
            await s.run_sync(Base.metadata.create_all)

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
    return HTMLResponse(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<input id="text" type="text">
<button onclick="sendMessage(event)">Send</button>

<script>
    let ws = new WebSocket("ws://localhost/api.poker/ws/1");

    ws.onopen = (event) => {
        console.log("connected");
    };
    ws.onmessage = (event) => {
        console.log(event.data);
    }

    function sendMessage(event) {
        const msg1 = {
            event: "game",
            payload: {
                "to_filter": "session",
            }
        }
        const msg2 = {
            event: "game",
            payload: {
                "to_filter": "allin",
            }
        }
        const msg3 = {
            event: "game",
            payload: {
                "to_filter":  "mecards",
            }
        }
        const msg4 = {
            event: "game",
            payload: {
                "to_filter": "tablecards",
            }
        }
        
        if (document.getElementById("text").value == 1) {
            ws.send(JSON.stringify(msg1));   
        } else if (document.getElementById("text").value == 2) {
            ws.send(JSON.stringify(msg2));
        } else if (document.getElementById("text").value == 3) {
            ws.send(JSON.stringify(msg3));
        } else if (document.getElementById("text").value == 4) {
            ws.send(JSON.stringify(msg4));
        }
        event.preventDefault();
    }
</script>
</body>
</html>
"""
    )
