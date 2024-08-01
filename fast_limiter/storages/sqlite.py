import time
from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional
from ..config import env_settings
from ..exceptions import StorageError
from .storage import Storage


class SQLRateLimit(SQLModel, table=True):
    key: str = Field(primary_key=True)
    count: int = Field(default=0)
    timestamp: float = Field(default=time.time())


class SQLiteStorage(Storage):
    """SQLite storage implementation for the rate limiter."""

    def __init__(self, db_path: str = env_settings.db_path):
        """
        Initializes the SQLite storage.

        Args:
            db_path (str): Path to the SQLite database file (default: "rtl.db").
        """
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}")
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    async def increment(self, key: str, increment: int = 1) -> int:
        """
        Increments the counter for the given key and returns the new value.

        Args:
            key (str): Unique key to identify the rate limit.
            increment (int): Value to increment (default: 1).

        Returns:
            int: The new counter value after incrementing.

        Raises:
            StorageError: If an error occurs while interacting with the SQLite database.
        """
        try:
            with self.session:
                rate_limit = self.session.get(SQLRateLimit, key)
                if rate_limit:
                    rate_limit.count += increment
                else:
                    rate_limit = SQLRateLimit(key=key, count=increment)
                rate_limit.timestamp = time.time()
                self.session.add(rate_limit)
                self.session.commit()
                return rate_limit.count
        except Exception as e:
            raise StorageError(f"Error incrementing counter in SQLite: {e}")

    async def get_remaining(self, key: str, limit: int, interval: int) -> int:
        """
        Returns the number of requests remaining within the interval.

        Args:
            key (str): Unique key to identify the rate limit.
            limit (int): Maximum number of requests allowed in the interval.
            interval (int): Time interval in seconds.

        Returns:
            int: The number of remaining requests.

        Raises:
            StorageError: If an error occurs while interacting with the SQLite database.
        """
        try:
            with self.session:
                rate_limit = self.session.get(SQLRateLimit, key)
                if rate_limit:
                    count = rate_limit.count
                    timestamp = rate_limit.timestamp
                    if time.time() - timestamp < interval:
                        return max(limit - count, 0)
                    else:
                        self.reset(key)
                return limit
        except Exception as e:
            raise StorageError(f"Error retrieving counter from SQLite: {e}")

    async def reset(self, key: str):
        """
        Resets the counter for the given key.

        Args:
            key (str): Unique key to identify the rate limit.

        Raises:
            StorageError: If an error occurs while interacting with the SQLite database.
        """
        try:
            with self.session:
                rate_limit = self.session.get(SQLRateLimit, key)
                if rate_limit:
                    self.session.delete(rate_limit)
                    self.session.commit()
        except Exception as e:
            raise StorageError(f"Error resetting counter in SQLite: {e}")

    async def get_timestamp(self, key: str) -> Optional[float]:
        """
        Gets the timestamp of the last request for the given key.

        Args:
            key (str): Unique key to identify the rate limit.

        Returns:
            Optional[float]: The timestamp of the last request, or None if not set.

        Raises:
            StorageError: If an error occurs while interacting with the SQLite database.
        """
        try:
            with self.session:
                rate_limit = self.session.get(SQLRateLimit, key)
                return rate_limit.timestamp if rate_limit else None
        except Exception as e:
            raise StorageError(f"Error retrieving timestamp from SQLite: {e}")

    async def set_timestamp(self, key: str):
        """
        Sets the timestamp of the last request for the given key.

        Args:
            key (str): Unique key to identify the rate limit.

        Raises:
            StorageError: If an error occurs while interacting with the SQLite database.
        """
        try:
            with self.session:
                rate_limit = self.session.get(SQLRateLimit, key)
                if rate_limit:
                    rate_limit.timestamp = time.time()
                else:
                    rate_limit = SQLRateLimit(key=key, timestamp=time.time())
                self.session.add(rate_limit)
                self.session.commit()
        except Exception as e:
            raise StorageError(f"Error setting timestamp in SQLite: {e}")

    def close(self):
        """
        Closes the SQLite connection.
        """
        self.session.close()
