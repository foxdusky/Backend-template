from sqlmodel import SQLModel


class AuthToken(SQLModel):
    access_token: str
