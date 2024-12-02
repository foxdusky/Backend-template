from sqlmodel import Session, select

from schemes.user.user_scheme import User


def get_user_by_username(session: Session, username: str) -> User | None:
    st = select(User).where(User.username == username)
    return session.exec(st).first()


def get_user_by_id(session: Session, user_id: int) -> User | None:
    st = select(User)
    st = st.where(User.id == user_id)
    return session.exec(st).first()
