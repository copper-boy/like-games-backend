from typing import Dict, Tuple

from pydantic import BaseConfig, BaseModel


class LikeEventSchema(BaseModel):
    class Config(BaseConfig):
        use_enum_values = True

    def dict(self, *args: Tuple, **kwargs: Dict) -> Dict:
        as_dict = super(LikeEventSchema, self).dict(*args, **kwargs, exclude_none=True)
        return as_dict
