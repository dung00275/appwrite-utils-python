"""
Appwrite Utils - A collection of utilities and extensions for Appwrite.

This package provides enhanced functionality for working with Appwrite services,
including simplified client management, database utilities, file operations,
and authentication helpers.
"""

__version__ = "0.1.0"
__author__ = "Dung Vu"
__email__ = "hoangdung00275@gmail.com"

from .client import AppwriteClient
from .database import DatabaseUtils
from .files import FileUtils
from .auth import AuthUtils
from .config import Config
from .exceptions import AppwriteException, ErrorHandler
from .types import (
    DocumentData,
    FileData,
    UserData,
    QueryBuilder,
    BatchResult,
    PaginationResult,
)

__all__ = [
    # Main classes
    "AppwriteClient",
    "DatabaseUtils", 
    "FileUtils",
    "AuthUtils",
    "Config",
    
    # Exceptions
    "AppwriteException",
    "ErrorHandler",
    
    # Types
    "DocumentData",
    "FileData", 
    "UserData",
    "QueryBuilder",
    "BatchResult",
    "PaginationResult",
    
    # Version info
    "__version__",
    "__author__",
    "__email__",
] 