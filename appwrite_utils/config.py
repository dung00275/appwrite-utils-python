"""
Configuration management for Appwrite Utils.

This module handles configuration settings, environment variables, and client setup.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration class for Appwrite Utils."""
    
    endpoint: str
    project_id: str
    api_key: str
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    max_batch_size: int = 100
    enable_logging: bool = True
    log_level: str = "INFO"
    custom_headers: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls(
            endpoint=os.getenv("APPWRITE_ENDPOINT", "https://cloud.appwrite.io/v1"),
            project_id=os.getenv("APPWRITE_PROJECT_ID", ""),
            api_key=os.getenv("APPWRITE_API_KEY", ""),
            timeout=int(os.getenv("APPWRITE_TIMEOUT", "30")),
            retry_attempts=int(os.getenv("APPWRITE_RETRY_ATTEMPTS", "3")),
            retry_delay=float(os.getenv("APPWRITE_RETRY_DELAY", "1.0")),
            max_batch_size=int(os.getenv("APPWRITE_MAX_BATCH_SIZE", "100")),
            enable_logging=os.getenv("APPWRITE_ENABLE_LOGGING", "true").lower() == "true",
            log_level=os.getenv("APPWRITE_LOG_LEVEL", "INFO"),
        )
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.project_id:
            raise ValueError("Project ID is required")
        
        if not self.api_key:
            raise ValueError("API key is required")
        
        if not self.endpoint:
            raise ValueError("Endpoint is required")
        
        if self.timeout <= 0:
            raise ValueError("Timeout must be greater than 0")
        
        if self.retry_attempts < 0:
            raise ValueError("Retry attempts must be non-negative")
        
        if self.retry_delay < 0:
            raise ValueError("Retry delay must be non-negative")
        
        if self.max_batch_size <= 0:
            raise ValueError("Max batch size must be greater than 0")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "endpoint": self.endpoint,
            "project_id": self.project_id,
            "api_key": self.api_key,
            "timeout": self.timeout,
            "retry_attempts": self.retry_attempts,
            "retry_delay": self.retry_delay,
            "max_batch_size": self.max_batch_size,
            "enable_logging": self.enable_logging,
            "log_level": self.log_level,
            "custom_headers": self.custom_headers,
        }
    
    def get_safe_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary without sensitive data."""
        config_dict = self.to_dict()
        config_dict["api_key"] = "***" if config_dict["api_key"] else ""
        return config_dict


class ConfigManager:
    """Manager for handling multiple configurations."""
    
    def __init__(self):
        self._configs: Dict[str, Config] = {}
        self._default_config: Optional[str] = None
    
    def add_config(self, name: str, config: Config) -> None:
        """Add a configuration with a name."""
        config.validate()
        self._configs[name] = config
        
        if not self._default_config:
            self._default_config = name
    
    def get_config(self, name: Optional[str] = None) -> Config:
        """Get configuration by name or default."""
        config_name = name or self._default_config
        
        if not config_name:
            raise ValueError("No default configuration set")
        
        if config_name not in self._configs:
            raise ValueError(f"Configuration '{config_name}' not found")
        
        return self._configs[config_name]
    
    def set_default(self, name: str) -> None:
        """Set default configuration."""
        if name not in self._configs:
            raise ValueError(f"Configuration '{name}' not found")
        
        self._default_config = name
    
    def list_configs(self) -> list:
        """List all configuration names."""
        return list(self._configs.keys())
    
    def remove_config(self, name: str) -> None:
        """Remove a configuration."""
        if name in self._configs:
            del self._configs[name]
            
            if self._default_config == name:
                self._default_config = list(self._configs.keys())[0] if self._configs else None


# Global configuration manager instance
config_manager = ConfigManager() 