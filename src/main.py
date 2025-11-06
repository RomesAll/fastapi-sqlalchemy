from database import Base, async_engine, engine, session_factory
from models import *
from sqlalchemy import select, text
import asyncio


async def setup_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def insert_workers():
    async with session_factory() as session:
        workers1 = WorkersORM(username='Roman')
        workers2 = WorkersORM(username='Jack')
        workers3 = WorkersORM(username='Misha')
        workers4 = WorkersORM(username='Nikita')
        session.add_all([workers1, workers2, workers3, workers4])
        await session.flush()
        await session.commit()
    
async def select_workers():
    async with session_factory() as session:
        query = select(WorkersORM)
        result = await session.execute(query)
        workers = result.scalars().all()
        print(workers)

async def main():
    await setup_db()
    await insert_workers()
    await asyncio.gather(select_workers())

asyncio.run(main())