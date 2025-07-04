"""
Enhanced Appwrite client with additional functionality.

This module provides an enhanced client that wraps the official Appwrite SDK
with additional features like retry logic, better error handling, and logging.
"""

import time
import logging
from typing import Optional, Dict, Any, Union
from appwrite.client import Client as AppwriteSDKClient
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.services.account import Account
from appwrite.services.users import Users
from appwrite.services.teams import Teams
from appwrite.services.functions import Functions
from appwrite.services.locale import Locale
from appwrite.services.avatars import Avatars
from appwrite.services.health import Health

from .config import Config
from .exceptions import AppwriteException, ErrorHandler, ConfigurationError


class AppwriteClient:
    """Enhanced Appwrite client with additional functionality."""
    
    def __init__(
        self,
        endpoint: Optional[str] = None,
        project_id: Optional[str] = None,
        api_key: Optional[str] = None,
        config: Optional[Config] = None
    ):
        """Initialize the enhanced Appwrite client."""
        if config:
            self.config = config
        else:
            self.config = Config(
                endpoint=endpoint or "https://cloud.appwrite.io/v1",
                project_id=project_id or "",
                api_key=api_key or ""
            )
        
        self.config.validate()
        self._setup_logging()
        self._setup_client()
        self._setup_services()
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        if self.config.enable_logging:
            logging.basicConfig(
                level=getattr(logging, self.config.log_level),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = None
    
    def _setup_client(self) -> None:
        """Setup the underlying Appwrite client."""
        try:
            self._client = AppwriteSDKClient()
            self._client.set_endpoint(self.config.endpoint)
            self._client.set_project(self.config.project_id)
            self._client.set_key(self.config.api_key)
            
            # Set custom headers if provided
            for key, value in self.config.custom_headers.items():
                self._client.add_header(key, value)
            
            if self.logger:
                self.logger.info("Appwrite client initialized successfully")
                
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize Appwrite client: {str(e)}")
    
    def _setup_services(self) -> None:
        """Setup Appwrite services."""
        self.databases = Databases(self._client)
        self.storage = Storage(self._client)
        self.account = Account(self._client)
        self.users = Users(self._client)
        self.teams = Teams(self._client)
        self.functions = Functions(self._client)
        self.locale = Locale(self._client)
        self.avatars = Avatars(self._client)
        self.health = Health(self._client)
    
    def execute_with_retry(self, operation, *args, **kwargs) -> Any:
        """Execute an operation with retry logic."""
        appwrite_error = None
        
        for attempt in range(self.config.retry_attempts + 1):
            try:
                return operation(*args, **kwargs)
                
            except Exception as e:
                appwrite_error = ErrorHandler.handle_appwrite_error(e)
                
                if not ErrorHandler.is_retryable_error(appwrite_error) or attempt == self.config.retry_attempts:
                    break
                
                if self.logger:
                    self.logger.warning(
                        f"Operation failed (attempt {attempt + 1}/{self.config.retry_attempts + 1}): {str(e)}"
                    )
                
                time.sleep(self.config.retry_delay * (2 ** attempt))  # Exponential backoff
        
        # If we get here, all retries failed
        if appwrite_error is not None:
            raise appwrite_error
        else:
            raise Exception("Operation failed after all retry attempts")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the Appwrite instance."""
        try:
            result = self.execute_with_retry(self.health.get)
            # Convert result to dict if it's not already
            if isinstance(result, dict):
                return result
            else:
                return {"status": "healthy", "response": str(result)}
        except Exception as e:
            if self.logger:
                self.logger.error(f"Health check failed: {str(e)}")
            raise
    
    def get_project_info(self) -> Dict[str, Any]:
        """Get project information."""
        try:
            # This would require additional API calls to get project details
            # For now, return basic info
            return {
                "project_id": self.config.project_id,
                "endpoint": self.config.endpoint,
                "config": self.config.get_safe_dict()
            }
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get project info: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """Test the connection to Appwrite."""
        try:
            self.health_check()
            if self.logger:
                self.logger.info("Connection test successful")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def get_client(self) -> AppwriteSDKClient:
        """Get the underlying Appwrite client."""
        return self._client
    
    def update_config(self, **kwargs) -> None:
        """Update configuration settings."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        self.config.validate()
        
        # Re-setup client if endpoint or credentials changed
        if any(key in kwargs for key in ['endpoint', 'project_id', 'api_key']):
            self._setup_client()
            self._setup_services()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        # Cleanup if needed
        pass 