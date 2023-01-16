from pydantic import BaseModel


class ReactionBase(BaseModel):
    is_like: bool = None


class Reaction(ReactionBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
