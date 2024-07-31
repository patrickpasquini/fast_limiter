import pytest
import pytest_asyncio
from fast_limiter.storages import SQLiteStorage
from fast_limiter.exceptions import StorageError


@pytest_asyncio.fixture
async def sql_storage(tmpdir):
    db_path = str(tmpdir.join("rtl.db"))
    storage = SQLiteStorage(db_path=db_path)
    yield storage
    storage.close()


@pytest.mark.asyncio
async def test_sqlite_increment_error(key: str, sql_storage: SQLiteStorage):
    try:
        await sql_storage.increment(key)
    except StorageError as e:
        assert "Error incrementing counter in SQLite" in str(e)


@pytest.mark.asyncio
async def test_sql_storage_get_remaining_error(
    key: str, sql_storage: SQLiteStorage
):
    try:
        await sql_storage.get_remaining(key, 10, 60)
    except StorageError as e:
        assert "Error retrieving counter from SQLite" in str(e)


@pytest.mark.asyncio
async def test_sql_storage_reset_error(key: str, sql_storage: SQLiteStorage):
    try:
        await sql_storage.reset(key)
    except StorageError as e:
        assert "Error resetting counter in SQLite" in str(e)


@pytest.mark.asyncio
async def test_sql_storage_get_timestamp_error(
    key: str, sql_storage: SQLiteStorage
):

    try:
        await sql_storage.get_timestamp(key)
    except StorageError as e:
        assert "Error retrieving timestamp from SQLite" in str(e)


@pytest.mark.asyncio
async def test_sql_storage_set_timestamp_error(
    key: str, sql_storage: SQLiteStorage
):
    try:
        await sql_storage.set_timestamp(key)
    except StorageError as e:
        assert "Error setting timestamp in SQLite" in str(e)
