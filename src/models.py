from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text
from typing import Annotated
from database import Base
import datetime, enum

id_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, 
                       mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, 
                       mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow)]

class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"

class WorkersORM(Base):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    created: Mapped[created_at]
    updated: Mapped[updated_at]

    resumes: Mapped[list["ResumesORM"]] = relationship(back_populates="workers")

class ResumesORM(Base):
    __tablename__ = "resumes"
    id: Mapped[id_pk]
    title: Mapped[str]
    compensation: Mapped[None | int]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created: Mapped[created_at]
    updated: Mapped[updated_at]

    workers: Mapped["WorkersORM"] = relationship(back_populates="resumes")
    vacancies_replied: Mapped[list["VacanciesORM"]] = relationship(
        back_populates="resumes_replied",
        secondary="vacancies_replies",
    )

class VacanciesORM(Base):
    __tablename__ = "vacancies"
    id: Mapped[id_pk]
    title: Mapped[str]
    compensation: Mapped[None | int]

    resumes_replied: Mapped[list["ResumesORM"]] = relationship(
        back_populates="vacancies_replied",
        secondary="vacancies_replies",
    )

class VacanciesRepliesOrm(Base):
    __tablename__ = "vacancies_replies"
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"), primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id", ondelete="CASCADE"), primary_key=True)
    cover_letter: Mapped[None | str]