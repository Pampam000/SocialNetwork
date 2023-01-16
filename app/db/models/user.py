from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from ..db_conf import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    birthdate = Column(Date, nullable=True)
    hashed_password = Column(String)

    posts = relationship("Post", back_populates="owner", cascade="all, delete")
    reactions = relationship("Reaction", back_populates="owner",
                             cascade="all, delete")
