from __future__ import annotations

from typing import Union

from pydantic import BaseModel


class PayloadSchema(BaseModel):
    data: Union[str, dict, list]
