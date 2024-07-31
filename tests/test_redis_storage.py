import time
import pytest
import pytest_asyncio
from fast_limiter.storages import RedisStorage


@pytest_asyncio.fixture
async def redis_storage():
    storage = RedisStorage(url="redis://localhost")
    yield storage
    await storage.db.flushall()
    await storage.db.aclose()


@pytest.mark.asyncio
async def test_redis_increment(key: str, redis_storage: RedisStorage):
    assert await redis_storage.increment(key) == 1
    assert await redis_storage.increment(key, 5) == 6


@pytest.mark.asyncio
async def test_redis_get_remaining(key: str, redis_storage: RedisStorage):
    limit = 10
    interval = 60
    assert await redis_storage.get_remaining(key, limit, interval) == 10
    await redis_storage.increment(key, 5)
    assert await redis_storage.get_remaining(key, limit, interval) == 5


@pytest.mark.asyncio
async def test_redis_reset(key: str, redis_storage: RedisStorage):
    limit = 10
    interval = 60
    await redis_storage.increment(key, 5)
    assert await redis_storage.get_remaining(key, limit, interval) == 5
    await redis_storage.reset(key)
    assert await redis_storage.get_remaining(key, limit, interval) == 10


@pytest.mark.asyncio
async def test_redis_get_timestamp(key: str, redis_storage: RedisStorage):
    await redis_storage.set_timestamp(key)
    timestamp = await redis_storage.get_timestamp(key)
    assert timestamp is not None
    assert abs(time.time() - timestamp) < 1
