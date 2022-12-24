from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from magic_filter import MagicFilter

from .mixins import LikeAsyncCallableMixin


@dataclass
class LikeFilterObject(LikeAsyncCallableMixin):
    magic: Optional[MagicFilter] = None

    def __post_init__(self) -> None:
        if isinstance(self.callback, MagicFilter):
            self.magic = self.callback
            self.callback = self.callback.resolve

        super(LikeFilterObject, self).__post_init__()
