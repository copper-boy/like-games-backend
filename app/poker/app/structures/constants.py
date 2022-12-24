from __future__ import annotations

CARD_RANK: dict[str, ...] = {"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"}
CARD_SUIT: dict[str, ...] = {"c", "d", "h", "s"}
CARD_MAX_DECK: int = len(CARD_RANK) * len(CARD_RANK)
