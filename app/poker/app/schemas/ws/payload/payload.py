from typing import Optional, Union

from pydantic import BaseModel


class WSPayloadSchema(BaseModel):
    to_filter: str

    data: Optional[Union[str, dict, list]]
