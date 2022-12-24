from magic_filter import MagicFilter

from .like import LikeRootRouter, LikeRouter

LikeF = MagicFilter()

__all__ = (
    "LikeRootRouter",
    "LikeRouter",
    "LikeF",
)
