from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import schemas
from config import ACCESS_TOKEN_EXPIRE_SECONDS, SECRET_KEY, ALGORITHM
from db.models import User
from db.crud import general
from db.db_conf import get_db
from .exceptions import INCORRECT_EMAIL_OR_PASSWORD, \
    COULD_NOT_VALIDATE_CREDENTIALS, USER_ALREADY_EXISTS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/log_in")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(db, email: str, password: str) -> User:
    user = general.get_instance_by(db=db, model=User, by='email',
                                   value=email)
    if not user or not verify_password(password, user.hashed_password):
        raise INCORRECT_EMAIL_OR_PASSWORD
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise COULD_NOT_VALIDATE_CREDENTIALS
        token_data = schemas.TokenData(username=email)
    except JWTError:
        raise COULD_NOT_VALIDATE_CREDENTIALS

    user = general.get_instance_by(db=db, model=User, by='email',
                                   value=token_data.username)
    if not user:
        raise COULD_NOT_VALIDATE_CREDENTIALS
    return user


def register_new_user(user_data: schemas.UserCreate, db: Session) -> str:
    if usr := general.get_instance_by(db=db, model=User, by='email',
                                      value=user_data.email):

        USER_ALREADY_EXISTS.detail = USER_ALREADY_EXISTS.detail.format(
            f"{usr.email}")
        raise USER_ALREADY_EXISTS

    user = User(email=user_data.email,
                hashed_password=hash_password(user_data.password))

    general.add_instance(db=db, item=user)

    return create_access_token(schemas.User.from_orm(user).dict())
