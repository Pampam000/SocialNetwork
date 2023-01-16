from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.db.crud import general
from app.db.db_conf import get_db
from app.helpers import auth
from app.schemas import User, UserBase

router = APIRouter(prefix='/user/{id}', tags=["user"])


@router.get("/me", response_model=User)
def get_me(current_user: User = Depends(auth.get_current_user)):
    return current_user


@router.put("/me", response_model=User)
def update_me(data: UserBase, db: Session = Depends(get_db),
              current_user: User = Depends(auth.get_current_user)):
    return general.update_instance(db=db, item=current_user, data=data.dict())


@router.delete("/me")
def delete_me(db: Session = Depends(get_db),
              current_user: User = Depends(auth.get_current_user)):
    general.delete_instance(db=db, item=current_user)

    return f"User {current_user.email} deleted successfully"
