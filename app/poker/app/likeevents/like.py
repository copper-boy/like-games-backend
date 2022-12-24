from __future__ import annotations

from .liketypes import LikeEventObserver
from .router import LikeRootRouter as _LikeRootRouter
from .router import LikeRouter as _LikeRouter


class LikeRouter(_LikeRouter):
    def __init__(self) -> None:
        super(LikeRouter, self).__init__()

        self.register("like_game", LikeEventObserver())
        self.register("like_helper", LikeEventObserver())


class LikeRootRouter(_LikeRootRouter, LikeRouter):
    ...
