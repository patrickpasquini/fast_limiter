import redis.asyncio as aioredis
import time
from typing import Optional
from ..config import env_settings
from ..exceptions import StorageError
from .storage import Storage


class RedisStorage(Storage):
    """Redis storage implementation for the rate limiter."""

    def __init__(self, url: str = env_settings.redis_url, prefix: str = "rtl"):
        """
        Initializes the Redis storage.

        Args:
            url (str): Connection URL for Redis (e.g., "redis://localhost").
            prefix (str): Prefix for the keys in Redis (optional, default: "rtl").
        """
        self.db = aioredis.from_url(url)
        self.prefix = prefix

    def _key(self, key: str) -> str:
        """Generates the full Redis key."""
        return f"{self.prefix}:{key}"

    async def increment(self, key: str, increment: int = 1) -> int:
        """
        Increments the counter for the given key and returns the new value.

        Args:
            key (str): Unique key to identify the rate limit.
            increment (int): Value to increment (default: 1).

        Returns:
            int: The new counter value after incrementing.

        Raises:
            StorageError: If an error occurs while communicating with Redis.
        """
        try:
            return await self.db.incrby(self._key(key), increment)
        except aioredis.RedisError as e:
            raise StorageError(f"Error incrementing counter in Redis: {e}")

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
            StorageError: If an error occurs while communicating with Redis.
        """
        try:
            count = await self.db.get(self._key(key))
            return limit if count is None else limit - int(count)
        except aioredis.RedisError as e:
            raise StorageError(f"Error retrieving counter from Redis: {e}")

    async def reset(self, key: str):
        """
        Resets the counter for the given key.

        Args:
            key (str): Unique key to identify the rate limit.

        Raises:
            StorageError: If an error occurs while communicating with Redis.
        """
        try:
            await self.db.delete(self._key(key))
        except aioredis.RedisError as e:
            raise StorageError(f"Error resetting counter in Redis: {e}")

    async def get_timestamp(self, key: str) -> Optional[float]:
        """
        Gets the timestamp of the last request for the given key.

        Args:
            key (str): Unique key to identify the rate limit.

        Returns:
            Optional[float]: The timestamp of the last request, or None if not set.

        Raises:
            StorageError: If an error occurs while communicating with Redis.
        """
        try:
            timestamp = await self.db.get(self._key(key) + "_ts")
            return float(timestamp) if timestamp else None
        except aioredis.RedisError as e:
            raise StorageError(f"Error retrieving timestamp from Redis: {e}")

    async def set_timestamp(self, key: str):
        """
        Sets the timestamp of the last request for the given key.

        Args:
            key (str): Unique key to identify the rate limit.

        Raises:
            StorageError: If an error occurs while communicating with Redis.
        """
        try:
            await self.db.set(self._key(key) + "_ts", time.time())
        except aioredis.RedisError as e:
            raise StorageError(f"Error setting timestamp in Redis: {e}")
