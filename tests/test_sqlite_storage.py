import time
import pytest
import pytest_asyncio
from fast_limiter.storages import SQLiteStorage


@pytest_asyncio.fixture
async def sql_storage(tmpdir):
    db_path = str(tmpdir.join("rtl.db"))
    storage = SQLiteStorage(db_path=db_path)
    yield storage
    storage.close()


@pytest.mark.asyncio
async def test_sqlite_increment(key: str, sql_storage: SQLiteStorage):
    assert await sql_storage.increment(key) == 1
    assert await sql_storage.increment(key, 5) == 6


@pytest.mark.asyncio
async def test_sqlite_get_remaining(key: str, sql_storage: SQLiteStorage):
    limit = 10
    interval = 60
    await sql_storage.increment(key)
    assert await sql_storage.get_remaining(key, limit, interval) == 9
    await sql_storage.increment(key, 5)
    assert await sql_storage.get_remaining(key, limit, interval) == 4


@pytest.mark.asyncio
async def test_sqlite_reset(key: str, sql_storage: SQLiteStorage):
    limit = 10
    interval = 60
    await sql_storage.increment(key, 5)
    assert await sql_storage.get_remaining(key, limit, interval) == 5
    await sql_storage.reset(key)
    assert await sql_storage.get_remaining(key, limit, interval) == 10


@pytest.mark.asyncio
async def test_get_timestamp(key: str, sql_storage: SQLiteStorage):
    await sql_storage.set_timestamp(key)
    timestamp = await sql_storage.get_timestamp(key)
    assert timestamp is not None
    assert abs(time.time() - timestamp) < 1
