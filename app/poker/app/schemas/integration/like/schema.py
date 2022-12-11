from pydantic import BaseModel


class LikeEvaluatorHandResponseSchema(BaseModel):
    id: int
    hand: str


class LikeEvaluatorRequestSchema(BaseModel):
    hands: list[str]
    board: list[str]


class LikeEvaluatorResponseSchema(BaseModel):
    winners: list[LikeEvaluatorHandResponseSchema]
