"""
Error handling for the PRC SDK.
"""

from .constants import ERROR_CODES


class PrcError(Exception):
    """Base exception for all PRC errors."""
    pass


class PrcApiError(PrcError):
    """Exception raised for PRC API errors."""
    
    def __init__(self, message, status_code, error_code=0):
        """
        Initialize a new PRC API error.
        
        Args:
            message: The error message.
            status_code: The HTTP status code.
            error_code: The PRC error code.
        """
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        
        
        detailed_message = ERROR_CODES.get(error_code, "")
        if detailed_message:
            message = f"{message} - {detailed_message}"
        
        super().__init__(f"[{status_code}] {message} (Error code: {error_code})")


class PrcConnectionError(PrcError):
    """Exception raised for connection errors."""
    
    def __init__(self, message="Failed to connect to the PRC API"):
        """
        Initialize a new connection error.
        
        Args:
            message: The error message.
        """
        self.message = message
        super().__init__(message)


class PrcRateLimitError(PrcApiError):
    """Exception raised for rate limit errors."""
    
    def __init__(self, retry_after=0):
        """
        Initialize a new rate limit error.
        
        Args:
            retry_after: The number of seconds to wait before retrying.
        """
        self.retry_after = retry_after
        message = f"Rate limit exceeded. Try again in {retry_after} seconds"
        super().__init__(message=message, status_code=429, error_code=4001)


class PrcAuthenticationError(PrcApiError):
    """Exception raised for authentication errors."""
    
    def __init__(self, error_code, message="Authentication failed"):
        """
        Initialize a new authentication error.
        
        Args:
            error_code: The specific authentication error code.
            message: The error message.
        """
        super().__init__(message=message, status_code=403, error_code=error_code)
