from sqlalchemy.orm import Session

from app.db.models import Post


def get_users_posts(db: Session, user_id: int) -> Session.query:
    return db.query(Post).filter(Post.owner_id == user_id).all()
