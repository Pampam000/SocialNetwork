from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

import schemas
from db import models
from db.crud import general, user
from db.db_conf import get_db
from helpers.exceptions import NOT_FOUND

router = APIRouter(prefix='/common', tags=["common"])


@router.get('/all_users', response_model=list[schemas.User])
async def get_all_users(db: Session = Depends(get_db)):
    return general.get_all(db=db, model=models.User)


@router.get('/all_posts', response_model=list[schemas.Post])
async def get_all_posts(db: Session = Depends(get_db)):
    return general.get_all(db=db, model=models.Post)


@router.get('/user/{id}/all_posts', response_model=list[schemas.Post])
async def get_all_users_posts(user_id: int = Query(..., ge=1),
                              db: Session = Depends(get_db)):
    if general.get_instance_by(db=db, model=models.User, by='id',
                               value=user_id):

        return user.get_users_posts(db=db, user_id=user_id)
    else:
        NOT_FOUND.detail = NOT_FOUND.detail.format("User", user_id)
        raise NOT_FOUND
