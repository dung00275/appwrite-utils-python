"""
File utilities for Appwrite.

This module provides enhanced file operations including batch uploads,
downloads, and file management utilities.
"""

import os
import mimetypes
from typing import List, Dict, Any, Optional, Union, BinaryIO
from pathlib import Path

from .exceptions import AppwriteException, ErrorHandler
from .types import FileData, BatchResult


class FileUtils:
    """Enhanced file utilities for Appwrite."""
    
    def __init__(self, client):
        """Initialize file utilities with an Appwrite client."""
        self.client = client
        self.storage = client.storage
        self.logger = getattr(client, 'logger', None)
    
    def upload_file(
        self,
        bucket_id: str,
        file_path: Union[str, Path],
        file_id: Optional[str] = None,
        permissions: Optional[List[str]] = None
    ) -> FileData:
        """Upload a file to Appwrite storage."""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Generate file ID if not provided
            if not file_id:
                file_id = "unique()"
            
            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if not mime_type:
                mime_type = "application/octet-stream"
            
            with open(file_path, 'rb') as file:
                result = self.client.execute_with_retry(
                    self.storage.create_file,
                    bucket_id,
                    file_id,
                    file,
                    permissions=permissions or []
                )
            
            if self.logger:
                self.logger.info(f"Successfully uploaded file: {file_path.name}")
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to upload file {file_path}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def upload_file_from_bytes(
        self,
        bucket_id: str,
        file_bytes: bytes,
        file_name: str,
        file_id: Optional[str] = None,
        mime_type: Optional[str] = None,
        permissions: Optional[List[str]] = None
    ) -> FileData:
        """Upload file from bytes data."""
        try:
            # Generate file ID if not provided
            if not file_id:
                file_id = "unique()"
            
            # Determine MIME type if not provided
            if not mime_type:
                mime_type, _ = mimetypes.guess_type(file_name)
                if not mime_type:
                    mime_type = "application/octet-stream"
            
            from io import BytesIO
            file_stream = BytesIO(file_bytes)
            
            result = self.client.execute_with_retry(
                self.storage.create_file,
                bucket_id,
                file_id,
                file_stream,
                permissions=permissions or []
            )
            
            if self.logger:
                self.logger.info(f"Successfully uploaded file from bytes: {file_name}")
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to upload file from bytes {file_name}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def download_file(
        self,
        bucket_id: str,
        file_id: str,
        destination_path: Union[str, Path]
    ) -> str:
        """Download a file from Appwrite storage."""
        try:
            destination_path = Path(destination_path)
            
            # Create directory if it doesn't exist
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            
            result = self.client.execute_with_retry(
                self.storage.get_file_download,
                bucket_id,
                file_id
            )
            
            # Write the file content
            with open(destination_path, 'wb') as file:
                file.write(result)
            
            if self.logger:
                self.logger.info(f"Successfully downloaded file to: {destination_path}")
            
            return str(destination_path)
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to download file {file_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def get_file_info(
        self,
        bucket_id: str,
        file_id: str
    ) -> FileData:
        """Get file information."""
        try:
            result = self.client.execute_with_retry(
                self.storage.get_file,
                bucket_id,
                file_id
            )
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get file info for {file_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def delete_file(
        self,
        bucket_id: str,
        file_id: str
    ) -> bool:
        """Delete a file from Appwrite storage."""
        try:
            self.client.execute_with_retry(
                self.storage.delete_file,
                bucket_id,
                file_id
            )
            
            if self.logger:
                self.logger.info(f"Successfully deleted file: {file_id}")
            
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to delete file {file_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def list_files(
        self,
        bucket_id: str,
        queries: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[FileData]:
        """List files in a bucket."""
        try:
            response = self.client.execute_with_retry(
                self.storage.list_files,
                bucket_id,
                queries=queries or [],
                limit=limit,
                offset=offset
            )
            
            return response.get('files', [])
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to list files in bucket {bucket_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def batch_upload_files(
        self,
        bucket_id: str,
        file_paths: List[Union[str, Path]],
        file_ids: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None
    ) -> BatchResult:
        """Upload multiple files in batch."""
        if not file_paths:
            return BatchResult(success_count=0, failure_count=0, errors=[], results=[])
        
        results = []
        errors = []
        success_count = 0
        failure_count = 0
        
        for i, file_path in enumerate(file_paths):
            try:
                file_id = file_ids[i] if file_ids and i < len(file_ids) else None
                
                result = self.upload_file(
                    bucket_id=bucket_id,
                    file_path=file_path,
                    file_id=file_id,
                    permissions=permissions
                )
                
                results.append(result)
                success_count += 1
                
            except Exception as e:
                error_info = {
                    "index": i,
                    "file_path": str(file_path),
                    "error": str(e)
                }
                errors.append(error_info)
                failure_count += 1
                
                if self.logger:
                    self.logger.error(f"Failed to upload file {file_path}: {str(e)}")
        
        if failure_count > 0 and self.logger:
            self.logger.warning(f"Batch upload completed with {failure_count} failures")
        
        return BatchResult(
            success_count=success_count,
            failure_count=failure_count,
            errors=errors,
            results=results
        )
    
    def batch_delete_files(
        self,
        bucket_id: str,
        file_ids: List[str]
    ) -> BatchResult:
        """Delete multiple files in batch."""
        if not file_ids:
            return BatchResult(success_count=0, failure_count=0, errors=[], results=[])
        
        results = []
        errors = []
        success_count = 0
        failure_count = 0
        
        for file_id in file_ids:
            try:
                result = self.delete_file(bucket_id, file_id)
                results.append({"file_id": file_id, "deleted": result})
                success_count += 1
                
            except Exception as e:
                error_info = {
                    "file_id": file_id,
                    "error": str(e)
                }
                errors.append(error_info)
                failure_count += 1
                
                if self.logger:
                    self.logger.error(f"Failed to delete file {file_id}: {str(e)}")
        
        if failure_count > 0 and self.logger:
            self.logger.warning(f"Batch delete completed with {failure_count} failures")
        
        return BatchResult(
            success_count=success_count,
            failure_count=failure_count,
            errors=errors,
            results=results
        )
    
    def get_file_url(
        self,
        bucket_id: str,
        file_id: str
    ) -> str:
        """Get the public URL for a file."""
        try:
            result = self.client.execute_with_retry(
                self.storage.get_file_view,
                bucket_id,
                file_id
            )
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get file URL for {file_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def update_file_permissions(
        self,
        bucket_id: str,
        file_id: str,
        permissions: List[str]
    ) -> FileData:
        """Update file permissions."""
        try:
            result = self.client.execute_with_retry(
                self.storage.update_file,
                bucket_id,
                file_id,
                permissions=permissions
            )
            
            if self.logger:
                self.logger.info(f"Successfully updated permissions for file: {file_id}")
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to update permissions for file {file_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e) 