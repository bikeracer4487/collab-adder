# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GitHub Collaborator Manager - A tkinter-based desktop application for managing GitHub repository collaborators using Personal Access Tokens.

## Development Commands

### Running the Application
```bash
python3 main.py
```

### Running Tests
```bash
# Run all tests
python3 -m unittest discover -s . -p "test_*.py"

# Run specific test file
python3 test_application.py
python3 test_github_client.py
python3 test_headless.py

# Run with pytest if available
python3 -m pytest
```

### Quick Start (macOS)
```bash
./start_macos.sh
```

## Architecture Overview

The application follows a modular architecture with clear separation of concerns:

1. **Entry Point (`main.py`)**: Handles dependency checking and launches the GUI. Always checks for `requests` module before importing the main application.

2. **GUI Layer (`src/main_app.py`)**: 
   - Implements `GitHubCollaboratorManager` class using tkinter
   - Uses threading for non-blocking API operations
   - All API calls are wrapped in `threading.Thread` to maintain UI responsiveness
   - Status updates use `root.after()` for thread-safe GUI updates

3. **API Client (`src/github_client.py`)**: 
   - Implements `GitHubAPIClient` class for all GitHub API v3 interactions
   - Methods: `authenticate()`, `get_user_repositories()`, `check_user_exists()`, `add_collaborator()`
   - Returns standardized response dictionaries with 'success' and 'message'/'data' keys

## Important Development Notes

- **Python Version**: Always use `python3` command (not `python`)
- **GUI Threading**: Any method that makes API calls must use `threading.Thread` to avoid freezing the UI
- **Error Handling**: All API operations return dictionaries with 'success' boolean and appropriate 'message' or 'data'
- **Token Security**: Personal Access Tokens are stored only in memory during runtime
- **Platform**: Optimized for macOS but maintains cross-platform compatibility

## Testing Approach

The project has three types of tests:
1. **Integration tests** (`test_application.py`): Tests the full application stack
2. **Unit tests** (`test_github_client.py`): Tests the API client in isolation
3. **Headless tests** (`test_headless.py`): For environments without GUI support

When modifying the application, ensure all three test suites pass.