from sqlmodel import create_engine, Session, SQLModel

from configs.env import DB_CON_STR

engine = create_engine(DB_CON_STR)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
