from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from schemas import Post, PostBase, User
from db.crud import user, general
from db.db_conf import get_db
from db import models
from helpers import auth
from helpers.exceptions import FORBIDDEN, NOT_FOUND

router = APIRouter(prefix='/user/{id}/posts', tags=["post"])


@router.get("/", response_model=list[Post])
def get_my_posts(db: Session = Depends(get_db),
                 current_user: User = Depends(auth.get_current_user)):
    return user.get_users_posts(db=db, user_id=current_user.id)


@router.post('/create', response_model=Post)
def create_post(post: PostBase, db: Session = Depends(get_db),
                current_user: User = Depends(auth.get_current_user)):
    p = models.Post(**post.dict(), owner_id=current_user.id)
    return general.add_instance(db=db, item=p)


@router.delete("/delete/{post_id}")
def delete_post(id_: int, db: Session = Depends(get_db),
                current_user: User = Depends(auth.get_current_user)):
    if post := general.get_instance_by(db=db, model=models.Post, by='id',
                                       value=id_):

        if post.owner_id == current_user.id:
            general.delete_instance(db=db, item=post)

            return f"post with id {id_} deleted successfully"
        else:
            FORBIDDEN.detail = FORBIDDEN.detail.format('delete', 'post', id_)
            raise FORBIDDEN

    else:
        NOT_FOUND.detail = NOT_FOUND.detail.format('post', id_)
        raise NOT_FOUND
