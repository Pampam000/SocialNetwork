from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import schemas
from db import models
from db.crud import general
from db.db_conf import get_db
from helpers import auth
from helpers.exceptions import NOT_FOUND
from schemas import User

router = APIRouter(prefix='/user/{id}/reactions', tags=["reaction"])


@router.post('/make_reaction')
def make_reaction(post_id: int, is_like: bool, db: Session = Depends(get_db),
                  current_user: User = Depends(auth.get_current_user)):
    if post := general.get_instance_by(db=db, model=models.Post, by='id',
                                       value=post_id):

        if post.owner_id != current_user.id:
            list_of_reaction_owners = [x.owner_id for x in post.reactions]

            if current_user.id not in list_of_reaction_owners:
                r = models.Reaction(is_like=is_like, owner_id=current_user.id,
                                    post_id=post.id)
                general.add_instance(db=db, item=r)

                return schemas.Post.from_orm(post)

            else:
                index = list_of_reaction_owners.index(current_user.id)
                item = post.reactions[index]

                if is_like == item.is_like:
                    general.delete_instance(db=db, item=item)
                    return schemas.Post.from_orm(post)
                else:
                    general.update_instance(db=db, item=item,
                                            data={'is_like': is_like})
                    return schemas.Post.from_orm(post)
        else:
            return "You could not like/dislike your own posts"

    else:
        raise NOT_FOUND
