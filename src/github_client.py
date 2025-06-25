"""
GitHub API Client for Collaborator Manager
Handles all GitHub API interactions including authentication, repository management, and collaborator operations.
"""

import requests
import json
from typing import List, Dict, Optional, Tuple


class GitHubAPIClient:
    """Client for interacting with GitHub API v4 (REST)"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = None
        self.headers = {}
        self.authenticated_user = None
    
    def authenticate(self, token: str) -> Tuple[bool, str]:
        """
        Authenticate with GitHub using Personal Access Token
        
        Args:
            token: GitHub Personal Access Token
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Collaborator-Manager"
        }
        
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                self.authenticated_user = response.json()
                return True, f"Successfully authenticated as {self.authenticated_user['login']}"
            elif response.status_code == 401:
                return False, "Invalid Personal Access Token"
            else:
                return False, f"Authentication failed: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Network error during authentication: {str(e)}"
    
    def get_user_repositories(self) -> Tuple[bool, List[Dict], str]:
        """
        Get all repositories for the authenticated user
        
        Returns:
            Tuple of (success: bool, repositories: List[Dict], message: str)
        """
        if not self.token:
            return False, [], "Not authenticated"
        
        repositories = []
        page = 1
        per_page = 100
        
        try:
            while True:
                response = requests.get(
                    f"{self.base_url}/user/repos",
                    headers=self.headers,
                    params={
                        "page": page,
                        "per_page": per_page,
                        "sort": "updated",
                        "type": "owner"  # Only repos owned by the user
                    },
                    timeout=10
                )
                
                if response.status_code != 200:
                    return False, [], f"Failed to fetch repositories: {response.status_code}"
                
                page_repos = response.json()
                if not page_repos:
                    break
                
                # Extract relevant repository information
                for repo in page_repos:
                    repositories.append({
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "description": repo.get("description", ""),
                        "private": repo["private"],
                        "url": repo["html_url"],
                        "permissions": repo.get("permissions", {})
                    })
                
                page += 1
                
                # GitHub API returns less than per_page items on the last page
                if len(page_repos) < per_page:
                    break
            
            return True, repositories, f"Found {len(repositories)} repositories"
            
        except requests.exceptions.RequestException as e:
            return False, [], f"Network error while fetching repositories: {str(e)}"
    
    def verify_username(self, username: str) -> Tuple[bool, str]:
        """
        Verify if a GitHub username exists
        
        Args:
            username: GitHub username to verify
            
        Returns:
            Tuple of (exists: bool, message: str)
        """
        if not username or not username.strip():
            return False, "Username cannot be empty"
        
        username = username.strip()
        
        try:
            response = requests.get(
                f"{self.base_url}/users/{username}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return True, f"User '{username}' found: {user_data.get('name', username)}"
            elif response.status_code == 404:
                return False, f"User '{username}' not found"
            else:
                return False, f"Error verifying username: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Network error while verifying username: {str(e)}"
    
    def add_collaborator(self, repo_full_name: str, username: str) -> Tuple[bool, str]:
        """
        Add a user as collaborator to a repository
        
        Args:
            repo_full_name: Full repository name (owner/repo)
            username: Username to add as collaborator
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.token:
            return False, "Not authenticated"
        
        try:
            response = requests.put(
                f"{self.base_url}/repos/{repo_full_name}/collaborators/{username}",
                headers=self.headers,
                json={"permission": "push"},  # Default to push permission
                timeout=10
            )
            
            if response.status_code == 201:
                return True, f"Successfully added {username} as collaborator to {repo_full_name}"
            elif response.status_code == 204:
                return True, f"{username} is already a collaborator on {repo_full_name}"
            elif response.status_code == 403:
                return False, f"Permission denied: Cannot add collaborators to {repo_full_name}"
            elif response.status_code == 404:
                return False, f"Repository {repo_full_name} not found or user {username} not found"
            elif response.status_code == 422:
                return False, f"Cannot add {username} as collaborator (may be repository owner)"
            else:
                return False, f"Failed to add collaborator: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Network error while adding collaborator: {str(e)}"
    
    def add_collaborators_bulk(self, repositories: List[str], username: str) -> List[Tuple[str, bool, str]]:
        """
        Add a user as collaborator to multiple repositories
        
        Args:
            repositories: List of repository full names
            username: Username to add as collaborator
            
        Returns:
            List of tuples (repo_name, success, message)
        """
        results = []
        
        for repo in repositories:
            success, message = self.add_collaborator(repo, username)
            results.append((repo, success, message))
        
        return results

