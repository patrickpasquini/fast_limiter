class StorageError(Exception):
    """Base exception for errors related to the rate limiter storage."""

    def __init__(self, message: str, original_exception: Exception = None):
        """
        Initializes the StorageError exception.

        Args:
            message (str): Descriptive error message.
            original_exception (Exception, optional): The original exception that caused this error.
        """
        super().__init__(message)
        self.original_exception = original_exception
