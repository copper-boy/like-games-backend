class BaseWSError(Exception):
    ...


class WSConnectionError(BaseWSError):
    ...


class WSAlreadyConnectedError(BaseWSError):
    ...
