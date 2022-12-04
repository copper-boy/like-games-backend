class BaseWSError(Exception):
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
