from datetime import datetime

from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    id: int | None = Field(primary_key=True)
    username: str | None
    password: str | None
    reg_at: datetime = Field(default_factory=datetime.utcnow)


class RegistrationRequest(SQLModel):
    username: str
    password: str


class UpdateUserRequest(SQLModel):
    id: int
    username: str | None = None
    password: str | None = None


class User(UserBase, table=True):
    __tablename__ = "user"
