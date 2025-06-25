#!/usr/bin/env python3
"""
Comprehensive test script for GitHub Collaborator Manager
Tests application structure, imports, and basic functionality
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)


class TestApplicationStructure(unittest.TestCase):
    """Test application file structure and imports"""
    
    def test_file_structure(self):
        """Test that all required files exist"""
        base_dir = os.path.dirname(__file__)
        
        required_files = [
            'main.py',
            'requirements.txt',
            'src/github_client.py',
            'src/main_app.py',
            'docs/architecture.md'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(base_dir, file_path)
            self.assertTrue(os.path.exists(full_path), f"Missing file: {file_path}")
    
    def test_imports(self):
        """Test that all modules can be imported"""
        try:
            from github_client import GitHubAPIClient
            from main_app import GitHubCollaboratorManager
            self.assertTrue(True, "All imports successful")
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_github_client_class(self):
        """Test GitHub client class structure"""
        from github_client import GitHubAPIClient
        
        client = GitHubAPIClient()
        
        # Test required methods exist
        required_methods = [
            'authenticate',
            'get_user_repositories',
            'verify_username',
            'add_collaborator',
            'add_collaborators_bulk'
        ]
        
        for method in required_methods:
            self.assertTrue(hasattr(client, method), f"Missing method: {method}")
    
    def test_gui_class_structure(self):
        """Test GUI class structure (without creating actual GUI)"""
        # Mock tkinter to avoid GUI creation
        with patch('tkinter.Tk'), patch('tkinter.ttk.Style'):
            from main_app import GitHubCollaboratorManager
            
            # Create mock root
            mock_root = Mock()
            mock_root.title = Mock()
            mock_root.geometry = Mock()
            mock_root.minsize = Mock()
            mock_root.configure = Mock()
            mock_root.grid_rowconfigure = Mock()
            mock_root.grid_columnconfigure = Mock()
            
            # Test class can be instantiated
            try:
                app = GitHubCollaboratorManager(mock_root)
                self.assertIsNotNone(app)
            except Exception as e:
                self.fail(f"Failed to create GUI class: {e}")


class TestGitHubClientFunctionality(unittest.TestCase):
    """Test GitHub client functionality"""
    
    def setUp(self):
        from github_client import GitHubAPIClient
        self.client = GitHubAPIClient()
    
    def test_client_initialization(self):
        """Test client initializes correctly"""
        self.assertEqual(self.client.base_url, "https://api.github.com")
        self.assertIsNone(self.client.token)
        self.assertIsNone(self.client.authenticated_user)
    
    def test_invalid_authentication(self):
        """Test authentication with invalid token"""
        success, message = self.client.authenticate("invalid_token")
        self.assertFalse(success)
        self.assertIn("Invalid Personal Access Token", message)
    
    def test_unauthenticated_operations(self):
        """Test operations without authentication"""
        # Test repository fetching
        success, repos, message = self.client.get_user_repositories()
        self.assertFalse(success)
        self.assertEqual(message, "Not authenticated")
        
        # Test collaborator addition
        success, message = self.client.add_collaborator("test/repo", "user")
        self.assertFalse(success)
        self.assertEqual(message, "Not authenticated")
    
    def test_username_validation(self):
        """Test username validation"""
        # Empty username
        exists, message = self.client.verify_username("")
        self.assertFalse(exists)
        self.assertIn("cannot be empty", message)
        
        # Whitespace username
        exists, message = self.client.verify_username("   ")
        self.assertFalse(exists)
        self.assertIn("cannot be empty", message)


class TestApplicationIntegration(unittest.TestCase):
    """Test application integration"""
    
    def test_main_entry_point(self):
        """Test main entry point can be imported"""
        try:
            # Import main module
            import main
            self.assertTrue(hasattr(main, 'main'))
            self.assertTrue(hasattr(main, 'check_dependencies'))
        except ImportError as e:
            self.fail(f"Failed to import main module: {e}")
    
    def test_dependency_check(self):
        """Test dependency checking"""
        import main
        
        deps_ok, error = main.check_dependencies()
        self.assertTrue(deps_ok, f"Dependencies not satisfied: {error}")


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestApplicationStructure,
        TestGitHubClientFunctionality,
        TestApplicationIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("GitHub Collaborator Manager - Comprehensive Test Suite")
    print("=" * 60)
    
    success = run_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All tests passed! Application is ready.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please check the output above.")
        sys.exit(1)

