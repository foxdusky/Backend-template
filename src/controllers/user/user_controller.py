from fastapi import APIRouter, Depends
from sqlmodel import Session

from constant.ws_queues import WSQueue
from db import get_session
from models.user import user_model
from models.user.auth_model import get_current_user
from models.user.auth_model import sign_in
from schemes.user.auth_scheme import AuthToken
from schemes.user.user_scheme import User, RegistrationRequest, UpdateUserRequest

queue_name = WSQueue.USER

user_router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@user_router.post(
    "/create/",
    response_model=AuthToken,
    description="Function for creating user exemplar in database by user him own self"
                " ||username: Require a unique name of user, also it's checking for unique",
    responses={
        200: {
            "description": "User successfully registered",
            "content": {"application/json": {"example": {"message": "Registration successful", "user_id": 1}}},
        },
        400: {
            "description": "Bad request - Possible reasons: non-unique username",
            "content": {
                "application/json": {
                    "examples": {
                        "non_unique_username": {"summary": "Username not unique",
                                                "value": {"detail": "Login: {username} is not unique"}},
                    }
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {"application/json": {"example": {"detail": "Internal server error"}}},
        },
    })
def registration(
    user: RegistrationRequest = Depends(),
    session: Session = Depends(get_session),
):
    password = user.password
    user = User(**user.model_dump())
    _user = user_model.create_user(session, user)
    token = sign_in(session, user.username, password)
    return token


@user_router.get("/current/", response_model=User, description="Func for getting info about current client")
async def get_current_user(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_model.get_user_by_id(session, current_user.id)


@user_router.get("/{client_id}", response_model=User, description="Func for getting info about client by his id")
async def get_user_by_id(
    client_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_model.get_user_by_id(session, client_id)


@user_router.put("/", response_model=User, description="Function for update profile by user him own self")
async def update_user(
    user: UpdateUserRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    user = User(**user.model_dump())
    return user_model.update_user(session, user, current_user)


@user_router.delete("/{user_id}", response_model=User, description="Function for delete profile by user him own self")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_model.delete_user(session, user_id, current_user)
