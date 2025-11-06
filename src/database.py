from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, MetaData
from config import settings

engine = create_engine(url=settings.DATABASE_URL_psycopg, echo=True)
async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)

class Base(DeclarativeBase):
    metadata = MetaData()

    def __repr__(self):
        data = []
        for ind, val in enumerate(self.__table__.columns.keys()):
            data.append(f"{val}={getattr(self, val)}")
        return f"<{self.__class__.__name__}({', '.join(data)})>"

session_factory = async_sessionmaker(async_engine)