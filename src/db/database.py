from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

class Base(DeclarativeBase):
    pass


db_url = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(db_url)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


