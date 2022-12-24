from __future__ import annotations

from .ws.builder import WSFactory


class Factory:
    def __init__(self) -> None:
        self.ws_factory = WSFactory()
