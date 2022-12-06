from .event import EventObserver


class LikeEventObserver(EventObserver):
    def __init__(self, event_name: str) -> None:
        super(LikeEventObserver, self).__init__()

        self.event_name = event_name
