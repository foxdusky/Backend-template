from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
from sqlmodel import Session

from configs.env import SECRET_KEY
from db import get_session
from repositories.user import auth_repository
from schemes.user.user_scheme import User
from schemes.user.auth_scheme import AuthToken

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/sign_in")

ALGORITHM = "HS256"
# 30 days
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60


def _get_password_hash(password: str) -> str:
    return password_context.hash(password)


def _is_correct_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def _authenticate_user(session: Session, username: str, password: str) -> User | None:
    user = auth_repository.get_user_by_username(session, username)
    if not user:
        return None
    if not _is_correct_password(password, user.password):
        return None
    return user


def _create_jwt_token(payload: dict, expiry: int | None = None):
    if expiry is None:
        expiration_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expiration_time = datetime.now() + timedelta(minutes=expiry)
    payload['exp'] = int(expiration_time.timestamp())
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def _get_auth_token(user_id: int, expiry: int | None = None) -> AuthToken:
    jwt_token = _create_jwt_token({"sub": str(user_id)}, expiry)
    return AuthToken(access_token=jwt_token)


def sign_in(session: Session, username: str, password: str):
    user = _authenticate_user(session, username, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return _get_auth_token(user.id)


def _verify_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        now_timestamp = int(datetime.now().timestamp())
        if decoded_token['exp'] < now_timestamp:
            return None
        else:
            user_id = int(decoded_token['sub'])
            return user_id

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
) -> User:
    user_id = _verify_jwt_token(token)
    user = auth_repository.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user.id} is not found"
        )
    return user
