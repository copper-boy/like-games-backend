from dataclasses import dataclass

from .mixins import AsyncCallableMixin


@dataclass
class HandlerObject(AsyncCallableMixin):
    to_filter: str

    def check(self, to_filter: str) -> bool:
        """
        Checks if the endpoint is suitable for the call

        :param to_filter:
          used to look for a match with an instance of a class
        :return:
          matching the `to_filter` parameter with the current instance of the class
        """
        return self.to_filter == to_filter
