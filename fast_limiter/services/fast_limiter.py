from functools import wraps
from fastapi import Request
from ..models import FastLimiter
from ..exceptions import LimiterError


def fast_limit(limiter: FastLimiter):
    """
    Decorator to apply rate limiting to a FastAPI route.

    Args:
        limiter (FastLimiter): Instance of FastLimiter that manages rate limiting.

    Returns:
        Callable: Decorated function that enforces rate limiting.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request", None)
            if request is None:
                raise LimiterError
            await limiter(request)
            return await func(*args, **kwargs)

        return wrapper

    return decorator
