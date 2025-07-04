#!/usr/bin/env python3
"""
Simple test script to verify the package structure and imports.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test importing the main modules."""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from appwrite_utils import AppwriteClient, DatabaseUtils, FileUtils, AuthUtils, Config
        print("✅ Basic imports successful")
        
        # Test exception imports
        from appwrite_utils import AppwriteException, ErrorHandler
        print("✅ Exception imports successful")
        
        # Test type imports
        from appwrite_utils import DocumentData, FileData, UserData, QueryBuilder, BatchResult, PaginationResult
        print("✅ Type imports successful")
        
        # Test configuration
        config = Config(
            endpoint="https://cloud.appwrite.io/v1",
            project_id="test-project",
            api_key="test-key"
        )
        print("✅ Configuration creation successful")
        
        # Test query builder
        query = QueryBuilder.equal("status", "active")
        print(f"✅ Query builder successful: {query}")
        
        # Test batch result
        batch_result = BatchResult(
            success_count=5,
            failure_count=0,
            errors=[],
            results=[]
        )
        print(f"✅ Batch result creation successful: {batch_result.success_count} successes")
        
        print("\n🎉 All imports and basic functionality tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_package_structure():
    """Test the package structure."""
    print("\nTesting package structure...")
    
    # Check if main package directory exists
    if os.path.exists("appwrite_utils"):
        print("✅ appwrite_utils directory exists")
    else:
        print("❌ appwrite_utils directory missing")
        return False
    
    # Check if __init__.py exists
    if os.path.exists("appwrite_utils/__init__.py"):
        print("✅ appwrite_utils/__init__.py exists")
    else:
        print("❌ appwrite_utils/__init__.py missing")
        return False
    
    # Check if main modules exist
    modules = ["client.py", "database.py", "files.py", "auth.py", "config.py", "exceptions.py", "types.py"]
    for module in modules:
        if os.path.exists(f"appwrite_utils/{module}"):
            print(f"✅ appwrite_utils/{module} exists")
        else:
            print(f"❌ appwrite_utils/{module} missing")
            return False
    
    print("✅ Package structure is correct!")
    return True

def main():
    """Main test function."""
    print("🧪 Testing Appwrite Utils Python Package")
    print("=" * 50)
    
    # Test package structure
    structure_ok = test_package_structure()
    
    # Test imports
    imports_ok = test_imports()
    
    if structure_ok and imports_ok:
        print("\n🎉 All tests passed! The package is ready to use.")
        print("\nNext steps:")
        print("1. Update the GitHub URLs in setup.py and pyproject.toml")
        print("2. Update author information in setup.py and pyproject.toml")
        print("3. Install the package: pip install -e .")
        print("4. Run the example: python examples/basic_usage.py")
        print("5. Run tests: python -m pytest tests/")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 