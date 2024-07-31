from fastapi import Request


class LimiterError(Exception):
    """Base exception for errors related to the rate limiter storage."""

    def __init__(self, original_exception: Exception = None):
        """
        Initializes the LimiterError exception.

        Args:
            original_exception (Exception, optional): The original exception that caused this error.
        """
        super().__init__(
            f"Missing 'request: {Request}' argument in rate_limit decorator"
        )
        self.original_exception = original_exception
