"""
Basic tests for Appwrite Utils.

This module contains basic tests for the Appwrite Utils library.
"""

import pytest
from unittest.mock import Mock, patch
from appwrite_utils import (
    AppwriteClient,
    DatabaseUtils,
    FileUtils,
    AuthUtils,
    Config,
    AppwriteException,
    ErrorHandler
)


class TestConfig:
    """Test configuration functionality."""
    
    def test_config_creation(self):
        """Test creating a configuration object."""
        config = Config(
            endpoint="https://test.appwrite.io/v1",
            project_id="test-project",
            api_key="test-key"
        )
        
        assert config.endpoint == "https://test.appwrite.io/v1"
        assert config.project_id == "test-project"
        assert config.api_key == "test-key"
        assert config.timeout == 30  # default value
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Should raise error for missing project_id
        with pytest.raises(ValueError, match="Project ID is required"):
            Config(
                endpoint="https://test.appwrite.io/v1",
                project_id="",
                api_key="test-key"
            )
        
        # Should raise error for missing api_key
        with pytest.raises(ValueError, match="API key is required"):
            Config(
                endpoint="https://test.appwrite.io/v1",
                project_id="test-project",
                api_key=""
            )
    
    def test_config_from_env(self):
        """Test creating configuration from environment variables."""
        with patch.dict('os.environ', {
            'APPWRITE_ENDPOINT': 'https://env.appwrite.io/v1',
            'APPWRITE_PROJECT_ID': 'env-project',
            'APPWRITE_API_KEY': 'env-key'
        }):
            config = Config.from_env()
            
            assert config.endpoint == "https://env.appwrite.io/v1"
            assert config.project_id == "env-project"
            assert config.api_key == "env-key"


class TestErrorHandler:
    """Test error handling functionality."""
    
    def test_handle_appwrite_error(self):
        """Test handling Appwrite errors."""
        # Test authentication error
        auth_error = Exception("401 Unauthorized")
        handled_error = ErrorHandler.handle_appwrite_error(auth_error)
        
        assert isinstance(handled_error, AppwriteException)
        assert handled_error.code == 401
        
        # Test not found error
        not_found_error = Exception("404 Not Found")
        handled_error = ErrorHandler.handle_appwrite_error(not_found_error)
        
        assert isinstance(handled_error, AppwriteException)
        assert handled_error.code == 404
    
    def test_is_retryable_error(self):
        """Test retryable error detection."""
        # Test retryable error
        retryable_error = AppwriteException("Rate limit exceeded", code=429)
        assert ErrorHandler.is_retryable_error(retryable_error) is True
        
        # Test non-retryable error
        non_retryable_error = AppwriteException("Not found", code=404)
        assert ErrorHandler.is_retryable_error(non_retryable_error) is False


class TestDatabaseUtils:
    """Test database utilities."""
    
    def setup_method(self):
        """Setup test method."""
        self.mock_client = Mock()
        self.mock_client.config.max_batch_size = 100
        self.mock_client.execute_with_retry = Mock()
        self.db_utils = DatabaseUtils(self.mock_client)
    
    def test_get_all_documents(self):
        """Test getting all documents."""
        # Mock response
        mock_response = {
            'documents': [
                {'$id': '1', 'name': 'John'},
                {'$id': '2', 'name': 'Jane'}
            ]
        }
        self.mock_client.execute_with_retry.return_value = mock_response
        
        result = self.db_utils.get_all_documents("users", limit=10)
        
        assert len(result) == 2
        assert result[0]['name'] == 'John'
        assert result[1]['name'] == 'Jane'
    
    def test_find_document(self):
        """Test finding a document."""
        # Mock response
        mock_response = {
            'documents': [{'$id': '1', 'name': 'John', 'email': 'john@example.com'}]
        }
        self.mock_client.execute_with_retry.return_value = mock_response
        
        result = self.db_utils.find_document("users", "email", "john@example.com")
        
        assert result is not None
        assert result['name'] == 'John'
        assert result['email'] == 'john@example.com'
    
    def test_find_document_not_found(self):
        """Test finding a document that doesn't exist."""
        # Mock empty response
        mock_response = {'documents': []}
        self.mock_client.execute_with_retry.return_value = mock_response
        
        result = self.db_utils.find_document("users", "email", "nonexistent@example.com")
        
        assert result is None


class TestFileUtils:
    """Test file utilities."""
    
    def setup_method(self):
        """Setup test method."""
        self.mock_client = Mock()
        self.mock_client.execute_with_retry = Mock()
        self.file_utils = FileUtils(self.mock_client)
    
    def test_upload_file_from_bytes(self):
        """Test uploading file from bytes."""
        # Mock response
        mock_response = {
            '$id': 'file123',
            'name': 'test.txt',
            'size': 15
        }
        self.mock_client.execute_with_retry.return_value = mock_response
        
        file_bytes = b"Hello, World!"
        result = self.file_utils.upload_file_from_bytes(
            bucket_id="test-bucket",
            file_bytes=file_bytes,
            file_name="test.txt"
        )
        
        assert result['$id'] == 'file123'
        assert result['name'] == 'test.txt'
        assert result['size'] == 15
    
    def test_get_file_info(self):
        """Test getting file information."""
        # Mock response
        mock_response = {
            '$id': 'file123',
            'name': 'test.txt',
            'size': 15,
            'mimeType': 'text/plain'
        }
        self.mock_client.execute_with_retry.return_value = mock_response
        
        result = self.file_utils.get_file_info("test-bucket", "file123")
        
        assert result['$id'] == 'file123'
        assert result['name'] == 'test.txt'
        assert result['mimeType'] == 'text/plain'


class TestAuthUtils:
    """Test authentication utilities."""
    
    def setup_method(self):
        """Setup test method."""
        self.mock_client = Mock()
        self.mock_client.execute_with_retry = Mock()
        self.auth_utils = AuthUtils(self.mock_client)
    
    def test_create_user_with_profile(self):
        """Test creating user with profile."""
        # Mock response
        mock_response = {
            '$id': 'user123',
            'email': 'test@example.com',
            'name': 'Test User'
        }
        self.mock_client.execute_with_retry.return_value = mock_response
        
        result = self.auth_utils.create_user_with_profile(
            email="test@example.com",
            password="password123",
            name="Test User"
        )
        
        assert result['$id'] == 'user123'
        assert result['email'] == 'test@example.com'
        assert result['name'] == 'Test User'
    
    def test_find_user_by_email(self):
        """Test finding user by email."""
        # Mock response
        mock_response = {
            'users': [{
                '$id': 'user123',
                'email': 'test@example.com',
                'name': 'Test User'
            }]
        }
        self.mock_client.execute_with_retry.return_value = mock_response
        
        result = self.auth_utils.find_user_by_email("test@example.com")
        
        assert result is not None
        assert result['$id'] == 'user123'
        assert result['email'] == 'test@example.com'
    
    def test_find_user_by_email_not_found(self):
        """Test finding user by email that doesn't exist."""
        # Mock empty response
        mock_response = {'users': []}
        self.mock_client.execute_with_retry.return_value = mock_response
        
        result = self.auth_utils.find_user_by_email("nonexistent@example.com")
        
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__]) 