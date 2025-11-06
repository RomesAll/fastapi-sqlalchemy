from database import Base, async_engine, engine
from models import *
from sqlalchemy import text
import asyncio


async def setup_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await setup_db()
    await asyncio.gather()

asyncio.run(main())