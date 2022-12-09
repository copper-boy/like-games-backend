from typing import Optional

from schemas import WSEventSchema
from structures.helpers import CallbackType
from structures.ws import WSConnection

from .event import EventObserver


class LikeEventObserver(EventObserver):
    def __init__(self, event_name: str, callback: Optional[CallbackType] = None) -> None:
        super(LikeEventObserver, self).__init__()

        self.event_name = event_name

        self.callback = callback

    async def trigger(self, data: WSEventSchema, ws: WSConnection) -> None:
        await super(LikeEventObserver, self).trigger(data=data, ws=ws)

        if self.callback:
            self.callback(ws=ws)
