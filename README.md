# GitHub Collaborator Manager

A sleek and responsive desktop application for managing GitHub repository collaborators using your Personal Access Token. Built specifically for Apple Silicon MacBook Pro, but compatible with other platforms.

## Features

- **Secure Authentication**: Uses your GitHub Personal Access Token for secure API access
- **Repository Management**: View and select from all your GitHub repositories
- **Username Verification**: Verify GitHub usernames before adding as collaborators
- **Bulk Operations**: Add users as collaborators to multiple repositories at once
- **Responsive Design**: Clean, modern interface optimized for macOS
- **Real-time Feedback**: Status updates and progress indicators for all operations
- **Error Handling**: Comprehensive error handling with user-friendly messages

## Screenshots

The application features a clean, modern interface with:
- Secure token input field (masked for security)
- Scrollable repository list with checkboxes
- Username verification with visual feedback
- Bulk collaborator addition with progress tracking
- Detailed status log for all operations

## Requirements

- **Operating System**: macOS (Apple Silicon MacBook Pro recommended), Linux, or Windows
- **Python**: Python 3.7 or higher
- **Dependencies**: 
  - `requests` (for GitHub API communication)
  - `tkinter` (for GUI - usually included with Python)

## Installation

### Option 1: Quick Start (Recommended)

1. **Download the application**:
   ```bash
   # Download or clone the application files to your desired location
   cd ~/Downloads  # or your preferred directory
   ```

2. **Install dependencies**:
   ```bash
   cd github_collaborator_manager
   pip3 install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 main.py
   ```

### Option 2: Manual Installation

1. **Ensure Python 3.7+ is installed**:
   ```bash
   python3 --version
   ```

2. **Install required packages**:
   ```bash
   pip3 install requests
   ```

3. **Verify tkinter is available**:
   ```bash
   python3 -c "import tkinter; print('tkinter is available')"
   ```

4. **Run the application**:
   ```bash
   python3 main.py
   ```

## Usage

### 1. Getting a GitHub Personal Access Token

Before using the application, you need a GitHub Personal Access Token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "Collaborator Manager")
4. Select the following scopes:
   - `repo` (Full control of private repositories)
   - `admin:org` (if you want to manage organization repositories)
5. Click "Generate token"
6. **Important**: Copy the token immediately - you won't be able to see it again!

### 2. Using the Application

1. **Launch the application**:
   ```bash
   python3 main.py
   ```

2. **Authenticate**:
   - Paste your Personal Access Token in the "Personal Access Token" field
   - Click "Authenticate"
   - The application will verify your token and load your repositories

3. **Select repositories**:
   - Browse through your repositories in the scrollable list
   - Use checkboxes to select repositories where you want to add collaborators
   - Use "Select All" or "Select None" buttons for convenience

4. **Verify username**:
   - Enter the GitHub username you want to add as a collaborator
   - Click "Verify User" to ensure the username exists and is spelled correctly
   - The status will show green checkmark for valid users

5. **Add collaborator**:
   - Once username is verified and repositories are selected, click "Add as Collaborator to Selected Repos"
   - The application will add the user to all selected repositories
   - Progress and results will be shown in the status log

### 3. Tips for Best Results

- **Token Security**: Never share your Personal Access Token. The application stores it only in memory during use.
- **Repository Permissions**: You can only add collaborators to repositories you own or have admin access to.
- **Username Verification**: Always verify usernames before adding to avoid typos.
- **Bulk Operations**: Select multiple repositories to add collaborators efficiently.
- **Status Monitoring**: Watch the status log for detailed feedback on each operation.

## Troubleshooting

### Common Issues

1. **"Invalid Personal Access Token"**:
   - Verify your token is correct and hasn't expired
   - Ensure the token has the required scopes (`repo` at minimum)

2. **"Permission denied" when adding collaborators**:
   - You can only add collaborators to repositories you own or have admin access to
   - Check if the repository is part of an organization with restricted permissions

3. **"User not found"**:
   - Verify the username is spelled correctly
   - The user must have a GitHub account

4. **Application won't start**:
   - Ensure Python 3.7+ is installed
   - Install required dependencies: `pip3 install requests`
   - On Linux, you may need: `sudo apt-get install python3-tk`

### Getting Help

If you encounter issues:

1. Check the status log in the application for detailed error messages
2. Verify your internet connection
3. Ensure your GitHub token has the correct permissions
4. Try with a single repository first to test functionality

## Security Notes

- **Token Storage**: Your Personal Access Token is only stored in memory while the application is running
- **API Limits**: The application respects GitHub's API rate limits
- **Permissions**: The application only requests the minimum necessary permissions
- **Local Operation**: All operations are performed locally - no data is sent to third parties

## Technical Details

- **Framework**: Python with tkinter for cross-platform GUI
- **API**: GitHub REST API v3
- **Architecture**: Modular design with separate API client and GUI components
- **Threading**: Non-blocking operations for responsive user interface
- **Error Handling**: Comprehensive error handling with user-friendly messages

## File Structure

```
github_collaborator_manager/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── github_client.py   # GitHub API client
│   └── main_app.py        # GUI application
├── docs/
│   └── architecture.md    # Technical documentation
└── test_headless.py       # Test suite
```

## License

This application is provided as-is for personal and educational use. Please respect GitHub's Terms of Service and API usage guidelines.

## Support

For issues or questions about this application, please check the troubleshooting section above or refer to the GitHub API documentation for API-related questions.

