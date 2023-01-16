from datetime import date

from pydantic import BaseModel

from .post import Post
from .reaction import Reaction


class UserBase(BaseModel):
    email: str
    birthdate: date = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    posts: list[Post] = []
    reactions: list[Reaction]

    class Config:
        orm_mode = True
