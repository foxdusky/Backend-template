from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from db import get_session
from models.user import auth_model, user_model
from schemes.user.user_scheme import User
from schemes.user.auth_scheme import AuthToken

auth_router = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)


@auth_router.post("/sign_in/", response_model=AuthToken)
async def sign_in(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    token = auth_model.sign_in(session, form_data.username, form_data.password)
    return token
