from fastapi import HTTPException, status

HEADERS = {"WWW-Authenticate": "Bearer"}

COULD_NOT_VALIDATE_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers=HEADERS
)

INCORRECT_EMAIL_OR_PASSWORD = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
    headers=HEADERS
)

USER_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail='User with email: {} is already exists',
    headers=HEADERS
)

NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='{} with id {} not found'
)

FORBIDDEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have not permissions to {} {} with id: {}"
)
