"""
Type definitions for Appwrite Utils.

This module contains custom types and type hints used throughout the library.
"""

from typing import Dict, List, Optional, Union, Any, TypedDict
from datetime import datetime
from dataclasses import dataclass


# DocumentData is a dictionary that can contain any Appwrite document fields
DocumentData = Dict[str, Any]


# FileData is a dictionary that can contain any Appwrite file fields
FileData = Dict[str, Any]


# UserData is a dictionary that can contain any Appwrite user fields
UserData = Dict[str, Any]


@dataclass
class BatchResult:
    """Result of a batch operation."""
    success_count: int
    failure_count: int
    errors: List[Dict[str, Any]]
    results: List[Any]


@dataclass
class PaginationResult:
    """Result of a paginated operation."""
    documents: List[DocumentData]
    total: int
    offset: int
    limit: int
    has_more: bool


class QueryBuilder:
    """Builder class for creating Appwrite queries."""
    
    @staticmethod
    def equal(attribute: str, value: Any) -> str:
        """Create an equal query."""
        return f'equal("{attribute}", "{value}")'
    
    @staticmethod
    def not_equal(attribute: str, value: Any) -> str:
        """Create a not equal query."""
        return f'notEqual("{attribute}", "{value}")'
    
    @staticmethod
    def less_than(attribute: str, value: Any) -> str:
        """Create a less than query."""
        return f'lessThan("{attribute}", "{value}")'
    
    @staticmethod
    def less_than_equal(attribute: str, value: Any) -> str:
        """Create a less than or equal query."""
        return f'lessThanEqual("{attribute}", "{value}")'
    
    @staticmethod
    def greater_than(attribute: str, value: Any) -> str:
        """Create a greater than query."""
        return f'greaterThan("{attribute}", "{value}")'
    
    @staticmethod
    def greater_than_equal(attribute: str, value: Any) -> str:
        """Create a greater than or equal query."""
        return f'greaterThanEqual("{attribute}", "{value}")'
    
    @staticmethod
    def search(attribute: str, value: str) -> str:
        """Create a search query."""
        return f'search("{attribute}", "{value}")'
    
    @staticmethod
    def order_asc(attribute: str) -> str:
        """Create an ascending order query."""
        return f'orderAsc("{attribute}")'
    
    @staticmethod
    def order_desc(attribute: str) -> str:
        """Create a descending order query."""
        return f'orderDesc("{attribute}")'
    
    @staticmethod
    def cursor_after(document_id: str) -> str:
        """Create a cursor after query."""
        return f'cursorAfter("{document_id}")'
    
    @staticmethod
    def cursor_before(document_id: str) -> str:
        """Create a cursor before query."""
        return f'cursorBefore("{document_id}")'
    
    @staticmethod
    def limit(value: int) -> str:
        """Create a limit query."""
        return f'limit({value})'
    
    @staticmethod
    def offset(value: int) -> str:
        """Create an offset query."""
        return f'offset({value})'


# Alias for backward compatibility
Query = QueryBuilder 