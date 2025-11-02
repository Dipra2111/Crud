
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    import models
    SQLModel.metadata.create_all(engine)
