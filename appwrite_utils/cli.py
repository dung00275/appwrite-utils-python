"""
Command-line interface for Appwrite Utils.

This module provides a simple CLI for common Appwrite operations.
"""

import argparse
import sys
import json
from typing import Optional

from . import AppwriteClient, DatabaseUtils, FileUtils, AuthUtils, Config


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Appwrite Utils - Enhanced utilities for Appwrite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test connection
  appwrite-utils test-connection

  # List documents
  appwrite-utils list-documents users

  # Upload file
  appwrite-utils upload-file bucket-id path/to/file.txt

  # Create user
  appwrite-utils create-user john@example.com password123 "John Doe"
        """
    )
    
    parser.add_argument(
        "--endpoint",
        default="https://cloud.appwrite.io/v1",
        help="Appwrite endpoint (default: https://cloud.appwrite.io/v1)"
    )
    parser.add_argument(
        "--project-id",
        required=True,
        help="Appwrite project ID"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="Appwrite API key"
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test connection command
    test_parser = subparsers.add_parser("test-connection", help="Test connection to Appwrite")
    
    # List documents command
    list_docs_parser = subparsers.add_parser("list-documents", help="List documents in a collection")
    list_docs_parser.add_argument("collection_id", help="Collection ID")
    list_docs_parser.add_argument("--limit", type=int, default=10, help="Number of documents to return")
    list_docs_parser.add_argument("--database-id", default="default", help="Database ID")
    
    # Upload file command
    upload_parser = subparsers.add_parser("upload-file", help="Upload a file")
    upload_parser.add_argument("bucket_id", help="Bucket ID")
    upload_parser.add_argument("file_path", help="Path to file to upload")
    upload_parser.add_argument("--file-id", help="Custom file ID")
    
    # Create user command
    create_user_parser = subparsers.add_parser("create-user", help="Create a user")
    create_user_parser.add_argument("email", help="User email")
    create_user_parser.add_argument("password", help="User password")
    create_user_parser.add_argument("name", help="User name")
    create_user_parser.add_argument("--phone", help="User phone number")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize client
        config = Config(
            endpoint=args.endpoint,
            project_id=args.project_id,
            api_key=args.api_key
        )
        
        client = AppwriteClient(config=config)
        
        # Execute command
        if args.command == "test-connection":
            result = test_connection(client)
        elif args.command == "list-documents":
            result = list_documents(client, args)
        elif args.command == "upload-file":
            result = upload_file(client, args)
        elif args.command == "create-user":
            result = create_user(client, args)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
        
        # Output result
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            print_result(result)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def test_connection(client: AppwriteClient) -> dict:
    """Test connection to Appwrite."""
    success = client.test_connection()
    return {
        "success": success,
        "message": "Connection successful" if success else "Connection failed"
    }


def list_documents(client: AppwriteClient, args) -> dict:
    """List documents in a collection."""
    db_utils = DatabaseUtils(client)
    documents = db_utils.get_all_documents(
        collection_id=args.collection_id,
        database_id=args.database_id,
        limit=args.limit
    )
    
    return {
        "collection_id": args.collection_id,
        "database_id": args.database_id,
        "count": len(documents),
        "documents": documents
    }


def upload_file(client: AppwriteClient, args) -> dict:
    """Upload a file."""
    file_utils = FileUtils(client)
    result = file_utils.upload_file(
        bucket_id=args.bucket_id,
        file_path=args.file_path,
        file_id=args.file_id
    )
    
    return {
        "bucket_id": args.bucket_id,
        "file_path": args.file_path,
        "result": result
    }


def create_user(client: AppwriteClient, args) -> dict:
    """Create a user."""
    auth_utils = AuthUtils(client)
    user_data = {
        "email": args.email,
        "password": args.password,
        "name": args.name
    }
    
    if args.phone:
        user_data["phone"] = args.phone
    
    result = auth_utils.create_user_with_profile(**user_data)
    
    return {
        "user": result
    }


def print_result(result: dict) -> None:
    """Print result in text format."""
    if "success" in result:
        status = "✅" if result["success"] else "❌"
        print(f"{status} {result['message']}")
    
    elif "count" in result:
        print(f"📊 Found {result['count']} documents in collection '{result['collection_id']}'")
        for doc in result["documents"]:
            print(f"  - {doc.get('$id', 'Unknown ID')}: {doc.get('name', 'No name')}")
    
    elif "result" in result and "name" in result["result"]:
        print(f"📁 File uploaded successfully: {result['result']['name']}")
        print(f"   File ID: {result['result'].get('$id', 'Unknown')}")
        print(f"   Size: {result['result'].get('size', 'Unknown')} bytes")
    
    elif "user" in result:
        user = result["user"]
        print(f"👤 User created successfully: {user.get('name', 'Unknown')}")
        print(f"   Email: {user.get('email', 'Unknown')}")
        print(f"   User ID: {user.get('$id', 'Unknown')}")


if __name__ == "__main__":
    main() 