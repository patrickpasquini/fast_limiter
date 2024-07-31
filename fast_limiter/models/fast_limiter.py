import time
from fastapi import Request, HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from ..storages import Storage


class FastLimiter:
    """Rate limiter class for managing request rate limiting."""

    def __init__(self, storage: Storage, limit: int, interval: int):
        """
        Initializes the FastLimiter.

        Args:
            storage (Storage): Instance of the storage to be used (e.g., RedisStorage or SQLiteStorage).
            limit (int): Maximum number of requests allowed within the interval.
            interval (int): Time interval in seconds during which requests are counted.
        """
        self.storage = storage
        self.limit = limit
        self.interval = interval

    async def __call__(self, request: Request):
        """
        Checks and enforces rate limiting based on the request.

        Args:
            request (Request): The incoming HTTP request.

        Raises:
            HTTPException: If the rate limit has been exceeded, raises HTTP 429 Too Many Requests exception
                with details about the time until reset.
        """
        client_ip = request.client.host
        key = f"{client_ip}:{request.url.path}"
        timestamp = await self.storage.get_timestamp(key)

        if timestamp and (time.time() - timestamp) > self.interval:
            await self.storage.reset(key)

        remaining = await self.storage.get_remaining(key, self.limit, self.interval)

        if remaining <= 0:
            reset_time = timestamp + self.interval
            time_until_reset = max(0, reset_time - time.time())
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many requests, please try again later. Time until reset: {time_until_reset:.2f} seconds.",
            )

        await self.storage.increment(key)
        await self.storage.set_timestamp(key)
