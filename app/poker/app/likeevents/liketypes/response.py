from __future__ import annotations

from typing import Any, NamedTuple

from likeevents.likeenums import LikeTriggerResultEnum


class LikeTriggerResponseNamedTuple(NamedTuple):
    handling: LikeTriggerResultEnum
    result: Any
