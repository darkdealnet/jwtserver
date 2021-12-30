from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from jwtserver.functions.config import load_config
config = load_config().db

sync_engine = create_engine(config.sync_url)
async_engine = create_async_engine(config.async_url)
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
