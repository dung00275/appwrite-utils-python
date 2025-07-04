"""
Database utilities for Appwrite.

This module provides enhanced database operations including batch processing,
pagination helpers, and simplified query building.
"""

import time
from typing import List, Dict, Any, Optional, Union
from appwrite.query import Query as AppwriteQuery

from .exceptions import AppwriteException, BatchOperationError, ErrorHandler
from .types import DocumentData, BatchResult, PaginationResult, QueryBuilder


class DatabaseUtils:
    """Enhanced database utilities for Appwrite."""
    
    def __init__(self, client):
        """Initialize database utilities with an Appwrite client."""
        self.client = client
        self.databases = client.databases
        self.logger = getattr(client, 'logger', None)
    
    def get_all_documents(
        self,
        collection_id: str,
        database_id: str = "default",
        queries: Optional[List[str]] = None,
        limit: int = -1
    ) -> List[DocumentData]:
        """Get all documents from a collection with pagination."""
        try:
            if limit > 0:
                queries = (queries or []) + [QueryBuilder.limit(limit)]
            
            response = self.client.execute_with_retry(
                    self.databases.list_documents,
                    database_id,
                    collection_id,
                    queries=queries or []
                )
                
            documents = response.get('documents', [])
            return documents
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get documents from {collection_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def get_documents_paginated(
        self,
        collection_id: str,
        database_id: str = "default",
        queries: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> PaginationResult:
        """Get documents with pagination information."""
        try:
            response = self.client.execute_with_retry(
                self.databases.list_documents,
                database_id,
                collection_id,
                queries=queries or [],
                limit=limit,
                offset=offset
            )
            
            return PaginationResult(
                documents=response.get('documents', []),
                total=response.get('total', 0),
                offset=offset,
                limit=limit,
                has_more=offset + limit < response.get('total', 0)
            )
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get paginated documents from {collection_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def batch_create_documents(
        self,
        collection_id: str,
        documents_data: List[Dict[str, Any]],
        database_id: str = "default",
        batch_size: Optional[int] = None
    ) -> BatchResult:
        """Create multiple documents in batches."""
        if not documents_data:
            return BatchResult(success_count=0, failure_count=0, errors=[], results=[])
        
        batch_size = batch_size or self.client.config.max_batch_size
        results = []
        errors = []
        success_count = 0
        failure_count = 0
        
        # Process in batches
        for i in range(0, len(documents_data), batch_size):
            batch = documents_data[i:i + batch_size]
            
            for doc_data in batch:
                try:
                    result = self.client.execute_with_retry(
                        self.databases.create_document,
                        database_id,
                        collection_id,
                        document_id="unique()",
                        data=doc_data
                    )
                    results.append(result)
                    success_count += 1
                    
                except Exception as e:
                    error_info = {
                        "index": len(results) + len(errors),
                        "data": doc_data,
                        "error": str(e)
                    }
                    errors.append(error_info)
                    failure_count += 1
                    
                    if self.logger:
                        self.logger.error(f"Failed to create document: {str(e)}")
        
        if failure_count > 0 and self.logger:
            self.logger.warning(f"Batch create completed with {failure_count} failures")
        
        return BatchResult(
            success_count=success_count,
            failure_count=failure_count,
            errors=errors,
            results=results
        )
    
    def batch_update_documents(
        self,
        collection_id: str,
        filter_query: str,
        update_data: Dict[str, Any],
        database_id: str = "default"
    ) -> int:
        """Update multiple documents that match a filter query."""
        try:
            # First, get all documents that match the filter
            documents = self.get_all_documents(
                collection_id=collection_id,
                database_id=database_id,
                queries=[filter_query]
            )
            
            updated_count = 0
            
            for document in documents:
                try:
                    self.client.execute_with_retry(
                        self.databases.update_document,
                        database_id,
                        collection_id,
                        document['$id'],
                        data=update_data
                    )
                    updated_count += 1
                    
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Failed to update document {document['$id']}: {str(e)}")
            
            if self.logger:
                self.logger.info(f"Updated {updated_count} documents in {collection_id}")
            
            return updated_count
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to batch update documents in {collection_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def batch_delete_documents(
        self,
        collection_id: str,
        filter_query: str,
        database_id: str = "default"
    ) -> int:
        """Delete multiple documents that match a filter query."""
        try:
            # First, get all documents that match the filter
            documents = self.get_all_documents(
                collection_id=collection_id,
                database_id=database_id,
                queries=[filter_query]
            )
            
            deleted_count = 0
            
            for document in documents:
                try:
                    self.client.execute_with_retry(
                        self.databases.delete_document,
                        database_id,
                        collection_id,
                        document['$id']
                    )
                    deleted_count += 1
                    
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Failed to delete document {document['$id']}: {str(e)}")
            
            if self.logger:
                self.logger.info(f"Deleted {deleted_count} documents from {collection_id}")
            
            return deleted_count
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to batch delete documents from {collection_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def find_document(
        self,
        collection_id: str,
        field: str,
        value: Any,
        database_id: str = "default"
    ) -> Optional[DocumentData]:
        """Find a single document by field value."""
        try:
            query = QueryBuilder.equal(field, value)
            response = self.client.execute_with_retry(
                self.databases.list_documents,
                database_id,
                collection_id,
                queries=[query],
                limit=1
            )
            
            documents = response.get('documents', [])
            return documents[0] if documents else None
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to find document in {collection_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def count_documents(
        self,
        collection_id: str,
        queries: Optional[List[str]] = None,
        database_id: str = "default"
    ) -> int:
        """Count documents in a collection with optional filters."""
        try:
            response = self.client.execute_with_retry(
                self.databases.list_documents,
                database_id,
                collection_id,
                queries=queries or [],
                limit=1
            )
            
            return response.get('total', 0)
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to count documents in {collection_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def document_exists(
        self,
        collection_id: str,
        document_id: str,
        database_id: str = "default"
    ) -> bool:
        """Check if a document exists."""
        try:
            self.client.execute_with_retry(
                self.databases.get_document,
                database_id,
                collection_id,
                document_id
            )
            return True
            
        except Exception as e:
            appwrite_error = ErrorHandler.handle_appwrite_error(e)
            if isinstance(appwrite_error, AppwriteException) and appwrite_error.code == 404:
                return False
            raise appwrite_error 

    def get_document_by_id(
        self,
        collection_id: str,
        document_id: str,
        database_id: str = "default"
    ) -> Optional[DocumentData]:
        """Get a single document by its ID."""
        try:
            return self.client.execute_with_retry(
                self.databases.get_document,
                database_id,
                collection_id,
                document_id
            )
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get document {document_id} in {collection_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)

    def update_document_by_id(
        self,
        collection_id: str,
        document_id: str,
        update_data: Dict[str, Any],
        database_id: str = "default"
    ) -> Optional[DocumentData]:
        """Update a single document by its ID."""
        try:
            return self.client.execute_with_retry(
                self.databases.update_document,
                database_id,
                collection_id,
                document_id,
                data=update_data
            )
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to update document {document_id} in {collection_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)

    def delete_document_by_id(
        self,
        collection_id: str,
        document_id: str,
        database_id: str = "default"
    ) -> bool:
        """Delete a single document by its ID."""
        try:
            self.client.execute_with_retry(
                self.databases.delete_document,
                database_id,
                collection_id,
                document_id
            )
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to delete document {document_id} in {collection_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)

    def update_document_by_query(
        self,
        collection_id: str,
        filter_query: str,
        update_data: Dict[str, Any],
        database_id: str = "default"
    ) -> Optional[DocumentData]:
        """Update the first document that matches a filter query. Raise error if none found."""
        # Get documents matching the query
        documents = self.get_all_documents(
            collection_id=collection_id,
            database_id=database_id,
            queries=[filter_query],
            limit=1
        )
        if not documents:
            raise ErrorHandler.handle_appwrite_error(Exception("No documents found for the given query."))
        document_id = documents[0].get("$id")
        if not document_id:
            raise ErrorHandler.handle_appwrite_error(Exception("Document does not have an $id field."))
        return self.update_document_by_id(
            collection_id=collection_id,
            document_id=document_id,
            update_data=update_data,
            database_id=database_id
        )

    def delete_documents_by_query(
        self,
        collection_id: str,
        filter_query: str,
        database_id: str = "default"
    ) -> int:
        """Delete multiple documents that match a filter query."""
        return self.batch_delete_documents(
            collection_id=collection_id,
            filter_query=filter_query,
            database_id=database_id
        ) 