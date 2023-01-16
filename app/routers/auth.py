from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import Token, UserCreate
from app.db.db_conf import get_db
from app.helpers import auth

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post("/log_in", response_model=Token)
def log_in(db: Session = Depends(get_db),
           form_data: OAuth2PasswordRequestForm = Depends()):

    user = auth.authenticate_user(db, form_data.username, form_data.password)
    access_token = auth.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/sign_up', status_code=status.HTTP_201_CREATED)
def sign_up(email: str, password: str, db: Session = Depends(get_db)):
    user = UserCreate(email=email, password=password)
    auth.register_new_user(db=db, user_data=user)
    return f"User {email} created"
