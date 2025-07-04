"""
Authentication utilities for Appwrite.

This module provides enhanced authentication operations including user management,
bulk operations, and authentication helpers.
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime

from .exceptions import AppwriteException, ErrorHandler
from .types import UserData, BatchResult


class AuthUtils:
    """Enhanced authentication utilities for Appwrite."""
    
    def __init__(self, client):
        """Initialize authentication utilities with an Appwrite client."""
        self.client = client
        self.users = client.users
        self.account = client.account
        self.logger = getattr(client, 'logger', None)
    
    def create_user_with_profile(
        self,
        email: str,
        password: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> UserData:
        """Create a user with profile information."""
        try:
            # Create the user
            user_data = {
                "email": email,
                "password": password,
                "name": name or "",
            }
            
            if phone:
                user_data["phone"] = phone
            
            user = self.client.execute_with_retry(
                self.users.create,
                user_id="unique()",
                **user_data
            )
            
            # Update with additional data if provided
            if additional_data:
                update_data = {}
                for key, value in additional_data.items():
                    if key not in ["email", "password", "name", "phone"]:
                        update_data[key] = value
                
                if update_data:
                    user = self.client.execute_with_retry(
                        self.users.update,
                        user["$id"],
                        **update_data
                    )
            
            if self.logger:
                self.logger.info(f"Successfully created user: {email}")
            
            return user
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to create user {email}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def bulk_create_users(
        self,
        users_data: List[Dict[str, Any]]
    ) -> BatchResult:
        """Create multiple users in batch."""
        if not users_data:
            return BatchResult(success_count=0, failure_count=0, errors=[], results=[])
        
        results = []
        errors = []
        success_count = 0
        failure_count = 0
        
        for i, user_data in enumerate(users_data):
            try:
                # Extract required fields
                email = user_data.get("email")
                password = user_data.get("password")
                name = user_data.get("name", "")
                
                if not email or not password:
                    raise ValueError("Email and password are required")
                
                # Create user
                result = self.create_user_with_profile(
                    email=email,
                    password=password,
                    name=name,
                    phone=user_data.get("phone"),
                    additional_data=user_data
                )
                
                results.append(result)
                success_count += 1
                
            except Exception as e:
                error_info = {
                    "index": i,
                    "user_data": user_data,
                    "error": str(e)
                }
                errors.append(error_info)
                failure_count += 1
                
                if self.logger:
                    self.logger.error(f"Failed to create user at index {i}: {str(e)}")
        
        if failure_count > 0 and self.logger:
            self.logger.warning(f"Bulk user creation completed with {failure_count} failures")
        
        return BatchResult(
            success_count=success_count,
            failure_count=failure_count,
            errors=errors,
            results=results
        )
    
    def find_user_by_email(
        self,
        email: str
    ) -> Optional[UserData]:
        """Find a user by email address."""
        try:
            response = self.client.execute_with_retry(
                self.users.list,
                queries=[f'equal("email", "{email}")'],
                limit=1
            )
            
            users = response.get('users', [])
            return users[0] if users else None
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to find user by email {email}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def find_user_by_phone(
        self,
        phone: str
    ) -> Optional[UserData]:
        """Find a user by phone number."""
        try:
            response = self.client.execute_with_retry(
                self.users.list,
                queries=[f'equal("phone", "{phone}")'],
                limit=1
            )
            
            users = response.get('users', [])
            return users[0] if users else None
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to find user by phone {phone}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def update_user_profile(
        self,
        user_id: str,
        profile_data: Dict[str, Any]
    ) -> UserData:
        """Update user profile information."""
        try:
            # Filter out non-updatable fields
            updatable_fields = ["name", "email", "phone", "password"]
            update_data = {k: v for k, v in profile_data.items() if k in updatable_fields}
            
            if not update_data:
                raise ValueError("No valid fields to update")
            
            result = self.client.execute_with_retry(
                self.users.update,
                user_id,
                **update_data
            )
            
            if self.logger:
                self.logger.info(f"Successfully updated user profile: {user_id}")
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to update user profile {user_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def delete_user(
        self,
        user_id: str
    ) -> bool:
        """Delete a user."""
        try:
            self.client.execute_with_retry(
                self.users.delete,
                user_id
            )
            
            if self.logger:
                self.logger.info(f"Successfully deleted user: {user_id}")
            
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to delete user {user_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def bulk_delete_users(
        self,
        user_ids: List[str]
    ) -> BatchResult:
        """Delete multiple users in batch."""
        if not user_ids:
            return BatchResult(success_count=0, failure_count=0, errors=[], results=[])
        
        results = []
        errors = []
        success_count = 0
        failure_count = 0
        
        for user_id in user_ids:
            try:
                result = self.delete_user(user_id)
                results.append({"user_id": user_id, "deleted": result})
                success_count += 1
                
            except Exception as e:
                error_info = {
                    "user_id": user_id,
                    "error": str(e)
                }
                errors.append(error_info)
                failure_count += 1
                
                if self.logger:
                    self.logger.error(f"Failed to delete user {user_id}: {str(e)}")
        
        if failure_count > 0 and self.logger:
            self.logger.warning(f"Bulk user deletion completed with {failure_count} failures")
        
        return BatchResult(
            success_count=success_count,
            failure_count=failure_count,
            errors=errors,
            results=results
        )
    
    def list_users(
        self,
        queries: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[UserData]:
        """List users with optional filters."""
        try:
            response = self.client.execute_with_retry(
                self.users.list,
                queries=queries or [],
                limit=limit,
                offset=offset
            )
            
            return response.get('users', [])
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to list users: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def get_user_sessions(
        self,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Get user sessions."""
        try:
            response = self.client.execute_with_retry(
                self.users.list_sessions,
                user_id
            )
            
            return response.get('sessions', [])
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get user sessions for {user_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def delete_user_sessions(
        self,
        user_id: str
    ) -> bool:
        """Delete all user sessions."""
        try:
            self.client.execute_with_retry(
                self.users.delete_sessions,
                user_id
            )
            
            if self.logger:
                self.logger.info(f"Successfully deleted all sessions for user: {user_id}")
            
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to delete user sessions for {user_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def update_user_status(
        self,
        user_id: str,
        status: str
    ) -> UserData:
        """Update user status (active, disabled, etc.)."""
        try:
            result = self.client.execute_with_retry(
                self.users.update_status,
                user_id,
                status
            )
            
            if self.logger:
                self.logger.info(f"Successfully updated user status to {status}: {user_id}")
            
            return result
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to update user status for {user_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e)
    
    def get_user_logs(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get user activity logs."""
        try:
            response = self.client.execute_with_retry(
                self.users.list_logs,
                user_id,
                limit=limit
            )
            
            return response.get('logs', [])
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to get user logs for {user_id}: {str(e)}")
            raise ErrorHandler.handle_appwrite_error(e) 