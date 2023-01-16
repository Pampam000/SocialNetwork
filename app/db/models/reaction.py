from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from ..db_conf import Base


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    is_like = Column(Boolean, default=None)

    owner_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    owner = relationship("User", back_populates="reactions")
    owner_post = relationship("Post", back_populates="reactions")
