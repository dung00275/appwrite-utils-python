# Appwrite Utils Python

A collection of utilities and extensions for Appwrite that makes working with Appwrite services easier and more efficient.

## Features

- **Enhanced Client Management**: Simplified client initialization and configuration
- **Database Utilities**: Helper functions for common database operations
- **File Management**: Extended file operations with better error handling
- **Authentication Helpers**: Streamlined authentication workflows
- **Batch Operations**: Efficient batch processing for multiple operations
- **Error Handling**: Improved error handling and logging
- **Type Hints**: Full type support for better development experience
- **Python 3.8+ Support**: Compatible with Python 3.8 and higher versions

## Installation

### From requirements.txt
If you have a `requirements.txt` file (for development or deployment), install dependencies with:

```bash
pip install -r requirements.txt
```

### From PyPI (when published)
```bash
pip install appwrite-utils
```

### From GitHub
```bash
pip install git+https://github.com/yourusername/appwrite-utils-python.git
```

### Development Installation
```bash
git clone https://github.com/yourusername/appwrite-utils-python.git
cd appwrite-utils-python
pip install -e .
```

## Requirements

- **Python**: 3.8 or higher
- **Appwrite SDK**: 7.1.0 or higher

## Quick Start

```python
from appwrite_utils import AppwriteClient, DatabaseUtils, FileUtils

# Initialize the client
client = AppwriteClient(
    endpoint="https://cloud.appwrite.io/v1",
    project_id="your-project-id",
    api_key="your-api-key"
)

# Use database utilities
db_utils = DatabaseUtils(client)
users = db_utils.get_all_documents("users", limit=100)

# Use file utilities
file_utils = FileUtils(client)
uploaded_file = file_utils.upload_file("bucket-id", "path/to/file.jpg")
```

## Usage Examples

### Database Operations

```python
from appwrite_utils import DatabaseUtils

db_utils = DatabaseUtils(client)

# Get all documents with pagination
documents = db_utils.get_all_documents(
    collection_id="users",
    queries=[
        Query.equal("status", "active"),
        Query.greater_than("created_at", "2023-01-01")
    ]
)

# Batch create documents
documents_data = [
    {"name": "John", "email": "john@example.com"},
    {"name": "Jane", "email": "jane@example.com"}
]
created_docs = db_utils.batch_create_documents("users", documents_data)

# Update multiple documents
update_data = {"status": "inactive"}
updated_count = db_utils.batch_update_documents(
    collection_id="users",
    filter_query=Query.equal("last_login", "2023-01-01"),
    update_data=update_data
)
```

### File Operations

```python
from appwrite_utils import FileUtils

file_utils = FileUtils(client)

# Upload file with metadata
file_info = file_utils.upload_file(
    bucket_id="images",
    file_path="path/to/image.jpg",
    file_id="unique-file-id",
    permissions=["read('team:admin')", "write('team:admin')"]
)

# Download file
file_utils.download_file("images", "file-id", "download/path.jpg")

# Get file with metadata
file_data = file_utils.get_file_with_metadata("images", "file-id")
```

### Authentication Helpers

```python
from appwrite_utils import AuthUtils

auth_utils = AuthUtils(client)

# Create user with additional data
user = auth_utils.create_user_with_profile(
    email="user@example.com",
    password="secure-password",
    name="John Doe",
    additional_data={"role": "admin", "department": "IT"}
)

# Bulk user operations
users_data = [
    {"email": "user1@example.com", "password": "pass1", "name": "User 1"},
    {"email": "user2@example.com", "password": "pass2", "name": "User 2"}
]
created_users = auth_utils.bulk_create_users(users_data)
```

## Configuration

You can configure the library using environment variables:

```bash
export APPWRITE_ENDPOINT="https://cloud.appwrite.io/v1"
export APPWRITE_PROJECT_ID="your-project-id"
export APPWRITE_API_KEY="your-api-key"
```

Or create a configuration file:

```python
from appwrite_utils import Config

config = Config(
    endpoint="https://cloud.appwrite.io/v1",
    project_id="your-project-id",
    api_key="your-api-key",
    timeout=30,
    retry_attempts=3
)
```

## Error Handling

The library provides enhanced error handling:

```python
from appwrite_utils import AppwriteException, ErrorHandler

try:
    result = db_utils.get_document("users", "user-id")
except AppwriteException as e:
    if e.code == 404:
        print("User not found")
    elif e.code == 401:
        print("Unauthorized access")
    else:
        print(f"Error: {e.message}")
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/appwrite-utils-python.git
cd appwrite-utils-python

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=appwrite_utils

# Run specific test file
pytest tests/test_database_utils.py
```

### Code Quality

```bash
# Format code
black appwrite_utils/

# Lint code
flake8 appwrite_utils/

# Type checking
mypy appwrite_utils/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://github.com/yourusername/appwrite-utils-python#readme)
- 🐛 [Bug Reports](https://github.com/yourusername/appwrite-utils-python/issues)
- 💡 [Feature Requests](https://github.com/yourusername/appwrite-utils-python/issues)
- 📧 [Email Support](mailto:hoangdung00275@gmail.com)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history. 