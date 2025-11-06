from database import Base, async_engine, engine, session_factory
from models import *
from sqlalchemy import Integer, and_, cast, insert, inspect, or_, select, text, update, func
from sqlalchemy.orm import aliased
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

async def update_workers(id: int = 2, username: str = 'Jack_new'):
    async with session_factory() as session:
        stmt = update(WorkersORM).where(WorkersORM.id == id).values(username=username)
        await session.execute(stmt)
        await session.commit()
        # workers = await session.get(WorkersORM, id)
        # workers.username = username
        # await session.commit()

async def insert_resumes():
    async with session_factory() as session:
        resume_jack_1 = ResumesORM(
            title="Python Junior Developer", compensation=50000, workload=Workload.fulltime, worker_id=1)
        resume_jack_2 = ResumesORM(
            title="Python Разработчик", compensation=150000, workload=Workload.fulltime, worker_id=1)
        resume_michael_1 = ResumesORM(
            title="Python Data Engineer", compensation=250000, workload=Workload.parttime, worker_id=2)
        resume_michael_2 = ResumesORM(
            title="Data Scientist", compensation=300000, workload=Workload.fulltime, worker_id=2)
        session.add_all([resume_jack_1, resume_jack_2, 
                        resume_michael_1, resume_michael_2])
        await session.commit()

async def select_resumes_avg_compensation(like_language: str = "Python"):
    """
    select workload, avg(compensation)::int as avg_compensation
    from resumes
    where title like '%Python%' and compensation > 40000
    group by workload
    having avg(compensation) > 70000
    """
    async with session_factory() as session:
        query = (
            select(
                ResumesORM.workload,
                func.avg(ResumesORM.compensation).cast(Integer).label('avg_comp'))
            .select_from(ResumesORM).filter(and_(ResumesORM.compensation > 40000, ResumesORM.title.contains(like_language)))
            .group_by(ResumesORM.workload)
            .having(func.avg(ResumesORM.compensation) > 70000)
        )
        avg_compensation = await session.execute(query)
        result = avg_compensation.all()
        print(result)

async def join_cte_subquery_window_func():
    """
    WITH helper2 AS (
        SELECT *, compensation-avg_workload_compensation AS compensation_diff
        FROM 
        (SELECT
            w.id,
            w.username,
            r.compensation,
            r.workload,
            avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
        FROM resumes r
        JOIN workers w ON r.worker_id = w.id) helper1
    )
    SELECT * FROM helper2
    ORDER BY compensation_diff DESC;
    """
    async with session_factory() as session:
        r = aliased(ResumesORM)
        w = aliased(WorkersORM)
        subq = (
            select(r, w, func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_compensation"))
            .join(r, r.worker_id == w.id).subquery("helper1")
        )
        cte = (
            select(
                subq.c.worker_id,
                subq.c.username,
                subq.c.compensation,
                subq.c.workload,
                subq.c.avg_workload_compensation,
                (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff")
            )
            .cte("helper2")
        )
        query = (
            select(cte)
            .order_by(cte.c.compensation_diff.desc())
        )
        result_query = await session.execute(query)
        result = result_query.all()
        print(result)

async def main():
    await setup_db()
    await insert_workers()
    await insert_resumes()

    await asyncio.gather(join_cte_subquery_window_func())

asyncio.run(main())