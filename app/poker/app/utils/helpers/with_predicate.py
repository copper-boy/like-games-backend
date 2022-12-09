from schemas import WSEventSchema
from structures.enums import RoundTypeEnum


async def with_predicate(
    first_operand: RoundTypeEnum, second_operand: RoundTypeEnum, event: WSEventSchema, manager
) -> None:
    if first_operand == second_operand:
        await manager.broadcast_json(event=event)
