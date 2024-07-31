from abc import ABC, abstractmethod
from typing import Optional


class Storage(ABC):
    """Abstract base class for rate limiter storage backends."""

    @abstractmethod
    async def get_remaining(self, key: str, limit: int, interval: int) -> int:
        """
        Returns the number of requests remaining within the interval.

        Args:
            key (str): Unique key to identify the rate limit.
            limit (int): Maximum number of requests allowed in the interval.
            interval (int): Time interval in seconds.

        Returns:
            int: The number of remaining requests.
        """
        ...

    @abstractmethod
    async def increment(self, key: str, increment: int = 1) -> int:
        """
        Increments the counter for the given key and returns the new value.

        Args:
            key (str): Unique key to identify the rate limit.
            increment (int): Value to increment (default: 1).

        Returns:
            int: The new counter value after incrementing.
        """
        ...

    @abstractmethod
    async def reset(self, key: str):
        """
        Resets the counter for the given key.

        Args:
            key (str): Unique key to identify the rate limit.
        """
        ...

    @abstractmethod
    async def get_timestamp(self, key: str) -> Optional[float]:
        """
        Gets the timestamp of the last request for the given key.

        Args:
            key (str): Unique key to identify the rate limit.

        Returns:
            Optional[float]: The timestamp of the last request, or None if not set.
        """
        ...

    @abstractmethod
    async def set_timestamp(self, key: str):
        """
        Sets the timestamp of the last request for the given key.

        Args:
            key (str): Unique key to identify the rate limit.
        """
        ...
