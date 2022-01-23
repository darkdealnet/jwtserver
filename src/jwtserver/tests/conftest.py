import asyncio
import aioredis
import pytest
from typing import AsyncGenerator, Any
from fastapi import FastAPI
from httpx import AsyncClient, Headers

from jwtserver import create_app
from jwtserver.dependencies.init_redis import redis_conn
from jwtserver.dependencies.session_db import async_db_session
from jwtserver.tests.depends import override_async_db_session, \
    override_redis_conn


@pytest.fixture(scope='module')
def event_loop():
    return asyncio.get_event_loop()


# @pytest.fixture(scope='session', autouse=True)
# def d_o():


# app.dependency_overrides[redis_client] = override_redis_client
# app.dependency_overrides[async_db_session] = override_async_db_session
# app.dependency_overrides[redis_conn] = override_redis_conn


@pytest.fixture(scope='module')
async def flushall():
    r = aioredis.from_url("redis://:@localhost:6380/1", decode_responses=True)
    await r.flushall()
    await r.close()


@pytest.fixture(scope='module')
def app() -> FastAPI:
    # settings = ApplicationSettings()
    # director = Director(DevelopmentApplicationBuilder(settings=settings))
    _app = create_app(lvl_logging='CRITICAL')
    _app.dependency_overrides[async_db_session] = override_async_db_session
    _app.dependency_overrides[redis_conn] = override_redis_conn
    return _app


@pytest.fixture(scope='module')
async def gen_client(app: FastAPI) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(
            app=app,
            # base_url="http://test",
            headers={'Content-Type': 'application/json'},
    ) as client:  # type: AsyncClient
        yield client


@pytest.fixture(scope='module')
def client(gen_client: AsyncClient) -> AsyncClient:
    return gen_client


@pytest.fixture(scope="module")
def authorized_client(gen_client: AsyncClient, token: str) -> AsyncClient:
    gen_client.headers = Headers({"Authorization": f"Bearer {token}"})
    return gen_client
