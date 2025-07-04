"""
Basic usage example for Appwrite Utils.

This example demonstrates the basic usage of the Appwrite Utils library.
"""

import os
from appwrite_utils import AppwriteClient, DatabaseUtils, FileUtils, AuthUtils, Config

def main():
    """Main example function."""
    
    # Method 1: Initialize with individual parameters
    client = AppwriteClient(
        endpoint="https://cloud.appwrite.io/v1",
        project_id="your-project-id",
        api_key="your-api-key"
    )
    
    # Method 2: Initialize with configuration object
    config = Config(
        endpoint="https://cloud.appwrite.io/v1",
        project_id="your-project-id",
        api_key="your-api-key",
        timeout=30,
        retry_attempts=3
    )
    
    client_with_config = AppwriteClient(config=config)
    
    # Method 3: Initialize from environment variables
    # Set these environment variables:
    # export APPWRITE_ENDPOINT="https://cloud.appwrite.io/v1"
    # export APPWRITE_PROJECT_ID="your-project-id"
    # export APPWRITE_API_KEY="your-api-key"
    
    config_from_env = Config.from_env()
    client_from_env = AppwriteClient(config=config_from_env)
    
    # Test connection
    if client.test_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")
        return
    
    # Initialize utilities
    db_utils = DatabaseUtils(client)
    file_utils = FileUtils(client)
    auth_utils = AuthUtils(client)
    
    # Database operations example
    print("\n📊 Database Operations:")
    
    # Get all documents from a collection
    try:
        documents = db_utils.get_all_documents(
            collection_id="users",
            limit=10
        )
        print(f"Found {len(documents)} documents")
    except Exception as e:
        print(f"Database operation failed: {e}")
    
    # Find a specific document
    try:
        user = db_utils.find_document(
            collection_id="users",
            field="email",
            value="user@example.com"
        )
        if user:
            print(f"Found user: {user.get('name', 'Unknown')}")
        else:
            print("User not found")
    except Exception as e:
        print(f"Find operation failed: {e}")
    
    # File operations example
    print("\n📁 File Operations:")
    
    # Upload a file
    try:
        # Create a test file
        with open("test_file.txt", "w") as f:
            f.write("Hello, Appwrite Utils!")
        
        uploaded_file = file_utils.upload_file(
            bucket_id="your-bucket-id",
            file_path="test_file.txt",
            file_id="test-file-123"
        )
        print(f"File uploaded: {uploaded_file.get('name', 'Unknown')}")
        
        # Clean up test file
        os.remove("test_file.txt")
        
    except Exception as e:
        print(f"File upload failed: {e}")
    
    # Authentication operations example
    print("\n👤 Authentication Operations:")
    
    # Create a user
    try:
        user = auth_utils.create_user_with_profile(
            email="test@example.com",
            password="secure-password",
            name="Test User",
            additional_data={"role": "user", "department": "IT"}
        )
        print(f"User created: {user.get('name', 'Unknown')}")
        
    except Exception as e:
        print(f"User creation failed: {e}")
    
    # Find user by email
    try:
        found_user = auth_utils.find_user_by_email("test@example.com")
        if found_user:
            print(f"Found user: {found_user.get('name', 'Unknown')}")
        else:
            print("User not found")
    except Exception as e:
        print(f"User search failed: {e}")
    
    # Batch operations example
    print("\n🔄 Batch Operations:")
    
    # Batch create documents
    try:
        documents_data = [
            {"name": "John Doe", "email": "john@example.com", "role": "admin"},
            {"name": "Jane Smith", "email": "jane@example.com", "role": "user"},
            {"name": "Bob Johnson", "email": "bob@example.com", "role": "user"}
        ]
        
        batch_result = db_utils.batch_create_documents(
            collection_id="users",
            documents_data=documents_data
        )
        
        print(f"Batch create: {batch_result.success_count} successful, {batch_result.failure_count} failed")
        
    except Exception as e:
        print(f"Batch operation failed: {e}")
    
    print("\n✅ Example completed!")

if __name__ == "__main__":
    main() 