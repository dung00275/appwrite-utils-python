"""
Custom exceptions for Appwrite Utils.

This module contains custom exception classes that provide better error handling
and more informative error messages for Appwrite operations.
"""

from typing import Optional, Dict, Any


class AppwriteException(Exception):
    """Base exception for Appwrite Utils."""
    
    def __init__(
        self,
        message: str,
        code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None
    ):
        self.message = message
        self.code = code
        self.response = response or {}
        self.original_exception = original_exception
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class ConfigurationError(AppwriteException):
    """Raised when there's a configuration error."""
    pass


class AuthenticationError(AppwriteException):
    """Raised when authentication fails."""
    pass


class PermissionError(AppwriteException):
    """Raised when permission is denied."""
    pass


class ValidationError(AppwriteException):
    """Raised when data validation fails."""
    pass


class NotFoundError(AppwriteException):
    """Raised when a resource is not found."""
    pass


class RateLimitError(AppwriteException):
    """Raised when rate limit is exceeded."""
    pass


class NetworkError(AppwriteException):
    """Raised when there's a network-related error."""
    pass


class BatchOperationError(AppwriteException):
    """Raised when a batch operation fails."""
    
    def __init__(
        self,
        message: str,
        success_count: int = 0,
        failure_count: int = 0,
        errors: Optional[list] = None
    ):
        self.success_count = success_count
        self.failure_count = failure_count
        self.errors = errors or []
        super().__init__(message)


class ErrorHandler:
    """Utility class for handling and transforming Appwrite errors."""
    
    @staticmethod
    def handle_appwrite_error(error: Exception) -> AppwriteException:
        """Convert Appwrite SDK errors to custom exceptions."""
        error_message = str(error)
        
        # Handle common Appwrite error patterns
        if "401" in error_message or "unauthorized" in error_message.lower():
            return AuthenticationError("Authentication failed", code=401)
        
        elif "403" in error_message or "forbidden" in error_message.lower():
            return PermissionError("Permission denied", code=403)
        
        elif "404" in error_message or "not found" in error_message.lower():
            return NotFoundError("Resource not found", code=404)
        
        elif "422" in error_message or "validation" in error_message.lower():
            return ValidationError("Validation failed", code=422)
        
        elif "429" in error_message or "rate limit" in error_message.lower():
            return RateLimitError("Rate limit exceeded", code=429)
        
        elif "network" in error_message.lower() or "connection" in error_message.lower():
            return NetworkError("Network error occurred", code=0)
        
        else:
            return AppwriteException(error_message, original_exception=error)
    
    @staticmethod
    def is_retryable_error(error: AppwriteException) -> bool:
        """Check if an error is retryable."""
        retryable_codes = [429, 500, 502, 503, 504]
        return error.code in retryable_codes or isinstance(error, NetworkError)
    
    @staticmethod
    def get_error_summary(error: AppwriteException) -> Dict[str, Any]:
        """Get a summary of the error for logging."""
        return {
            "message": error.message,
            "code": error.code,
            "type": type(error).__name__,
            "retryable": ErrorHandler.is_retryable_error(error)
        } 