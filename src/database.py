from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, MetaData
from config import settings

engine = create_engine(url=settings.DATABASE_URL_psycopg, echo=True)
async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)

class Base(DeclarativeBase):
    pass
    #metadata = MetaData()

session_factory = async_sessionmaker(async_engine)