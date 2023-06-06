from typing import AsyncGenerator

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.middleware.sessions import SessionMiddleware
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./instance/photo.db"
DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


SECRET_KEY = "20"
ALGORITHM = "HS256"

Base = declarative_base()


security = HTTPBearer()

Base.metadata.create_all(bind=engine)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
