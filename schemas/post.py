from pydantic import BaseModel
from .reaction import Reaction


class PostBase(BaseModel):
    title: str
    content: str


class Post(PostBase):
    id: int
    owner_id: int
    reactions: list[Reaction]

    class Config:
        orm_mode = True
