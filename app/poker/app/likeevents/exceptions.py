from __future__ import annotations


class LikeEventsError(BaseException):
    ...


class LikeRouterError(LikeEventsError):
    ...


class LikeRouterObserverError(LikeRouterError):
    ...


class LikeRouterRegisterError(LikeRouterError):
    ...


class LikeRouterObserverNotRegisteredError(LikeRouterError):
    ...


class LikeRouterObserverAlreadyRegisteredError(LikeRouterObserverError):
    ...
