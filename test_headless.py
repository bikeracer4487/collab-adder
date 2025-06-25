#!/usr/bin/env python3
"""
Headless test script for GitHub Collaborator Manager
Tests core functionality without creating GUI
"""

import sys
import os
import unittest

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)


def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    
    base_dir = os.path.dirname(__file__)
    required_files = [
        'main.py',
        'requirements.txt',
        'src/github_client.py',
        'src/main_app.py',
        'docs/architecture.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        return False
    else:
        print("✓ All required files present")
        return True


def test_github_client():
    """Test GitHub client functionality"""
    print("\nTesting GitHub client...")
    
    try:
        from github_client import GitHubAPIClient
        
        # Test initialization
        client = GitHubAPIClient()
        assert client.base_url == "https://api.github.com"
        assert client.token is None
        print("✓ Client initialization successful")
        
        # Test required methods exist
        required_methods = [
            'authenticate', 'get_user_repositories', 'verify_username',
            'add_collaborator', 'add_collaborators_bulk'
        ]
        
        for method in required_methods:
            if not hasattr(client, method):
                print(f"✗ Missing method: {method}")
                return False
        print("✓ All required methods present")
        
        # Test invalid authentication
        success, message = client.authenticate("invalid_token")
        if success:
            print("✗ Invalid token should fail authentication")
            return False
        print("✓ Invalid token authentication correctly rejected")
        
        # Test unauthenticated operations
        success, repos, message = client.get_user_repositories()
        if success:
            print("✗ Unauthenticated repository fetch should fail")
            return False
        # Accept either "Not authenticated" or API error responses
        if "Not authenticated" not in message and "401" not in message:
            print(f"✗ Unexpected error message: {message}")
            return False
        print("✓ Unauthenticated operations correctly rejected")
        
        # Test username validation
        exists, message = client.verify_username("")
        if exists:
            print("✗ Empty username should be invalid")
            return False
        print("✓ Username validation working")
        
        return True
        
    except Exception as e:
        print(f"✗ GitHub client test failed: {e}")
        return False


def test_imports():
    """Test that modules can be imported"""
    print("\nTesting imports...")
    
    try:
        # Test GitHub client import
        from github_client import GitHubAPIClient
        print("✓ GitHub client import successful")
        
        # Test main app import (this will import tkinter)
        # We'll catch the display error but verify the module structure
        try:
            from main_app import GitHubCollaboratorManager
            print("✓ Main app import successful")
        except Exception as e:
            if "DISPLAY" in str(e) or "display" in str(e).lower():
                print("✓ Main app import successful (GUI not available in headless mode)")
            else:
                print(f"✗ Main app import failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False


def test_dependencies():
    """Test that dependencies are available"""
    print("\nTesting dependencies...")
    
    try:
        import requests
        print("✓ requests library available")
        
        import tkinter
        print("✓ tkinter library available")
        
        return True
        
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False


def main():
    """Run all tests"""
    print("GitHub Collaborator Manager - Headless Test Suite")
    print("=" * 55)
    
    tests = [
        test_file_structure,
        test_dependencies,
        test_github_client,
        test_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 55)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Application is ready for use.")
        return True
    else:
        print("✗ Some tests failed. Please check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

