import os
from typing import AsyncGenerator
from pymongo import MongoClient

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


database_name = os.getenv("POSTGRES_DB", "posteet_db")
database_user = os.getenv("POSTGRES_USER", "user")
database_password = os.getenv("POSTGRES_PASSWORD", "pass")
database_port = os.getenv("POSTGRES_PORT", "5432")
database_host = os.getenv("POSTGRES_HOST", "db")

DATABASE_URL = f"postgresql+asyncpg://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"
MONGODB_URL = f"mongodb://admin:password@mongodb:27017/mongodb?authSource=admin"

Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


mongo_client = MongoClient(MONGODB_URL)
mongo_database = mongo_client["posteet_db"]