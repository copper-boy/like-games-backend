from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Adds to model table name attribute

        :return:
          generated table name attribute
        """

        return cls.__name__.lower()
