from typing import Optional, Union

from pydantic import BaseModel


class WSPayloadSchema(BaseModel):
    to_filter: Optional[str]

    data: Optional[Union[str, dict, list]]
