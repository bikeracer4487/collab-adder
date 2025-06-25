"""
Test script for GitHub API Client
This script tests the basic functionality without requiring a real token
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from github_client import GitHubAPIClient


def test_client_initialization():
    """Test client initialization"""
    client = GitHubAPIClient()
    assert client.base_url == "https://api.github.com"
    assert client.token is None
    assert client.authenticated_user is None
    print("✓ Client initialization test passed")


def test_authentication_invalid_token():
    """Test authentication with invalid token"""
    client = GitHubAPIClient()
    success, message = client.authenticate("invalid_token")
    assert not success
    assert "Invalid Personal Access Token" in message or "Authentication failed" in message
    print("✓ Invalid token authentication test passed")


def test_username_verification():
    """Test username verification (this will work without authentication)"""
    client = GitHubAPIClient()
    
    # Test with empty username
    exists, message = client.verify_username("")
    assert not exists
    assert "cannot be empty" in message
    print("✓ Empty username test passed")
    
    # Test with whitespace username
    exists, message = client.verify_username("   ")
    assert not exists
    assert "cannot be empty" in message
    print("✓ Whitespace username test passed")


def test_unauthenticated_operations():
    """Test operations that require authentication when not authenticated"""
    client = GitHubAPIClient()
    
    # Test getting repositories without authentication
    success, repos, message = client.get_user_repositories()
    assert not success
    assert "Not authenticated" in message
    print("✓ Unauthenticated repository fetch test passed")
    
    # Test adding collaborator without authentication
    success, message = client.add_collaborator("test/repo", "testuser")
    assert not success
    assert "Not authenticated" in message
    print("✓ Unauthenticated collaborator addition test passed")


if __name__ == "__main__":
    print("Running GitHub API Client tests...")
    print()
    
    try:
        test_client_initialization()
        test_authentication_invalid_token()
        test_username_verification()
        test_unauthenticated_operations()
        
        print()
        print("All tests passed! ✓")
        
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)

