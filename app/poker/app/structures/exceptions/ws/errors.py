class BaseWSError(Exception):
    ...


class WSEventError(BaseWSError):
    ...


class WSUnhandledEventError(WSEventError):
    ...


class WSUnhandledEndpointError(WSUnhandledEventError):
    ...


class WSMessageError(BaseWSError):
    ...


class WSCommandError(WSMessageError):
    ...


class WSStateError(BaseWSError):
    ...


class WSConnectionError(BaseWSError):
    ...


class WSAlreadyConnectedError(BaseWSError):
    ...
