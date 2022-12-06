from schemas import WSEventSchema
from structures.event import LikeEventObserver
from structures.ws import WSConnection


class Router:
    def __init__(self) -> None:
        self.action = LikeEventObserver(event_name="action")
        self.helper = LikeEventObserver(event_name="helper")

        self.observers: dict[str, LikeEventObserver] = {
            "action": self.action,
            "helper": self.helper,
        }

    async def event(self, data: WSEventSchema, ws: WSConnection) -> None:
        observer = self.observers[data.event]
        await observer.trigger(data=data, ws=ws)
