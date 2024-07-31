import pytest
import pytest_asyncio
from fast_limiter.storages import RedisStorage
from fast_limiter.exceptions import StorageError


@pytest_asyncio.fixture
async def redis_storage():
    storage = RedisStorage(url="redis://invalid-url")
    yield storage
    await storage.db.aclose()


@pytest.mark.asyncio
async def test_redis_storage_increment_error(key: str, redis_storage: RedisStorage):
    try:
        await redis_storage.increment(key)
    except StorageError as e:
        assert "Error incrementing counter in Redis" in str(e)


@pytest.mark.asyncio
async def test_redis_storage_get_remaining_error(key: str, redis_storage: RedisStorage):
    try:
        await redis_storage.get_remaining(key, 10, 60)
    except StorageError as e:
        assert "Error retrieving counter from Redis" in str(e)


@pytest.mark.asyncio
async def test_redis_storage_reset_error(key: str, redis_storage: RedisStorage):
    try:
        await redis_storage.reset(key)
    except StorageError as e:
        assert "Error resetting counter in Redis" in str(e)


@pytest.mark.asyncio
async def test_redis_storage_get_timestamp_error(key: str, redis_storage: RedisStorage):
    try:
        await redis_storage.get_timestamp(key)
    except StorageError as e:
        assert "Error retrieving timestamp from Redis" in str(e)


@pytest.mark.asyncio
async def test_redis_storage_set_timestamp_error(key: str, redis_storage: RedisStorage):
    try:
        await redis_storage.set_timestamp(key)
    except StorageError as e:
        assert "Error setting timestamp in Redis" in str(e)
