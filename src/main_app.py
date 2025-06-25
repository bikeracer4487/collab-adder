"""
GitHub Collaborator Manager - Main GUI Application
A sleek and responsive desktop application for managing GitHub repository collaborators.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from github_client import GitHubAPIClient


class GitHubCollaboratorManager:
    """Main application class for GitHub Collaborator Manager"""
    
    def __init__(self, root):
        self.root = root
        self.github_client = GitHubAPIClient()
        self.repositories = []
        self.repo_vars = {}  # Dictionary to store checkbox variables
        
        self.setup_window()
        self.create_widgets()
        self.setup_layout()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("GitHub Collaborator Manager")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Configure style for better appearance on macOS
        style = ttk.Style()
        style.theme_use('aqua' if sys.platform == 'darwin' else 'clam')
        
        # Configure colors and fonts
        self.root.configure(bg='#f0f0f0')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame, 
            text="GitHub Collaborator Manager",
            font=('Helvetica', 18, 'bold')
        )
        
        # Personal Access Token Section
        self.token_frame = ttk.LabelFrame(self.main_frame, text="Authentication", padding="10")
        
        self.token_label = ttk.Label(self.token_frame, text="Personal Access Token:")
        self.token_entry = ttk.Entry(self.token_frame, show="*", width=50)
        self.token_button = ttk.Button(
            self.token_frame, 
            text="Authenticate", 
            command=self.authenticate
        )
        
        # Repository Section
        self.repo_frame = ttk.LabelFrame(self.main_frame, text="Your Repositories", padding="10")
        
        # Repository list with scrollbar
        self.repo_list_frame = ttk.Frame(self.repo_frame)
        self.repo_canvas = tk.Canvas(self.repo_list_frame, height=200, bg='white')
        self.repo_scrollbar = ttk.Scrollbar(
            self.repo_list_frame, 
            orient="vertical", 
            command=self.repo_canvas.yview
        )
        self.repo_canvas.configure(yscrollcommand=self.repo_scrollbar.set)
        
        self.repo_inner_frame = ttk.Frame(self.repo_canvas)
        self.repo_canvas.create_window((0, 0), window=self.repo_inner_frame, anchor="nw")
        
        # Select all/none buttons
        self.repo_buttons_frame = ttk.Frame(self.repo_frame)
        self.select_all_button = ttk.Button(
            self.repo_buttons_frame, 
            text="Select All", 
            command=self.select_all_repos
        )
        self.select_none_button = ttk.Button(
            self.repo_buttons_frame, 
            text="Select None", 
            command=self.select_none_repos
        )
        
        # Username Verification Section
        self.user_frame = ttk.LabelFrame(self.main_frame, text="Add Collaborator", padding="10")
        
        self.username_label = ttk.Label(self.user_frame, text="GitHub Username:")
        self.username_entry = ttk.Entry(self.user_frame, width=30)
        self.verify_button = ttk.Button(
            self.user_frame, 
            text="Verify User", 
            command=self.verify_username
        )
        
        self.username_status = ttk.Label(
            self.user_frame, 
            text="", 
            foreground="gray"
        )
        
        # Add Collaborator Button
        self.add_button = ttk.Button(
            self.user_frame, 
            text="Add as Collaborator to Selected Repos", 
            command=self.add_collaborator,
            state="disabled"
        )
        
        # Status/Log Section
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Status", padding="10")
        
        self.status_text = scrolledtext.ScrolledText(
            self.status_frame, 
            height=8, 
            width=70,
            state="disabled"
        )
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.status_frame, 
            mode='indeterminate'
        )
    
    def setup_layout(self):
        """Arrange widgets in the window"""
        
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)  # Repository frame
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Token section
        self.token_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.token_frame.grid_columnconfigure(1, weight=1)
        
        self.token_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.token_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.token_button.grid(row=0, column=2)
        
        # Repository section
        self.repo_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.repo_frame.grid_rowconfigure(0, weight=1)
        self.repo_frame.grid_columnconfigure(0, weight=1)
        
        self.repo_list_frame.grid(row=0, column=0, sticky="nsew")
        self.repo_list_frame.grid_rowconfigure(0, weight=1)
        self.repo_list_frame.grid_columnconfigure(0, weight=1)
        
        self.repo_canvas.grid(row=0, column=0, sticky="nsew")
        self.repo_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.repo_buttons_frame.grid(row=1, column=0, pady=(10, 0))
        self.select_all_button.grid(row=0, column=0, padx=(0, 10))
        self.select_none_button.grid(row=0, column=1)
        
        # Username section
        self.user_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self.user_frame.grid_columnconfigure(1, weight=1)
        
        self.username_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.username_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.verify_button.grid(row=0, column=2)
        
        self.username_status.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))
        self.add_button.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        # Status section
        self.status_frame.grid(row=4, column=0, sticky="ew")
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_text.grid(row=0, column=0, sticky="ew")
        self.progress.grid(row=1, column=0, sticky="ew", pady=(10, 0))
    
    def log_message(self, message, level="info"):
        """Add a message to the status log"""
        self.status_text.config(state="normal")
        
        # Color coding for different message types
        if level == "error":
            color = "red"
        elif level == "success":
            color = "green"
        elif level == "warning":
            color = "orange"
        else:
            color = "black"
        
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
        
        # Update the window
        self.root.update_idletasks()
    
    def authenticate(self):
        """Authenticate with GitHub using the provided token"""
        token = self.token_entry.get().strip()
        
        if not token:
            messagebox.showerror("Error", "Please enter your Personal Access Token")
            return
        
        self.log_message("Authenticating with GitHub...")
        self.progress.start()
        self.token_button.config(state="disabled")
        
        def auth_thread():
            success, message = self.github_client.authenticate(token)
            
            # Update UI in main thread
            self.root.after(0, self.auth_complete, success, message)
        
        threading.Thread(target=auth_thread, daemon=True).start()
    
    def auth_complete(self, success, message):
        """Handle authentication completion"""
        self.progress.stop()
        self.token_button.config(state="normal")
        
        if success:
            self.log_message(message, "success")
            self.load_repositories()
        else:
            self.log_message(f"Authentication failed: {message}", "error")
            messagebox.showerror("Authentication Failed", message)
    
    def load_repositories(self):
        """Load user's repositories"""
        self.log_message("Loading repositories...")
        self.progress.start()
        
        def load_thread():
            success, repos, message = self.github_client.get_user_repositories()
            
            # Update UI in main thread
            self.root.after(0, self.repos_loaded, success, repos, message)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def repos_loaded(self, success, repos, message):
        """Handle repositories loading completion"""
        self.progress.stop()
        
        if success:
            self.repositories = repos
            self.display_repositories()
            self.log_message(message, "success")
        else:
            self.log_message(f"Failed to load repositories: {message}", "error")
            messagebox.showerror("Error", f"Failed to load repositories: {message}")
    
    def display_repositories(self):
        """Display repositories with checkboxes"""
        # Clear existing widgets
        for widget in self.repo_inner_frame.winfo_children():
            widget.destroy()
        
        self.repo_vars = {}
        
        for i, repo in enumerate(self.repositories):
            var = tk.BooleanVar()
            self.repo_vars[repo['full_name']] = var
            
            # Create checkbox with repository info
            checkbox = ttk.Checkbutton(
                self.repo_inner_frame,
                variable=var,
                text=f"{repo['name']} {'(Private)' if repo['private'] else '(Public)'}"
            )
            checkbox.grid(row=i, column=0, sticky="w", pady=2)
            
            # Add description if available
            if repo['description']:
                desc_label = ttk.Label(
                    self.repo_inner_frame,
                    text=f"  {repo['description'][:80]}{'...' if len(repo['description']) > 80 else ''}",
                    foreground="gray",
                    font=('Helvetica', 9)
                )
                desc_label.grid(row=i, column=1, sticky="w", padx=(10, 0))
        
        # Update scroll region
        self.repo_inner_frame.update_idletasks()
        self.repo_canvas.configure(scrollregion=self.repo_canvas.bbox("all"))
        
        # Bind mousewheel to canvas
        def on_mousewheel(event):
            self.repo_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.repo_canvas.bind("<MouseWheel>", on_mousewheel)
    
    def select_all_repos(self):
        """Select all repositories"""
        for var in self.repo_vars.values():
            var.set(True)
    
    def select_none_repos(self):
        """Deselect all repositories"""
        for var in self.repo_vars.values():
            var.set(False)
    
    def verify_username(self):
        """Verify the entered username"""
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username to verify")
            return
        
        self.log_message(f"Verifying username: {username}")
        self.verify_button.config(state="disabled")
        self.username_status.config(text="Verifying...", foreground="orange")
        
        def verify_thread():
            exists, message = self.github_client.verify_username(username)
            
            # Update UI in main thread
            self.root.after(0, self.username_verified, exists, message)
        
        threading.Thread(target=verify_thread, daemon=True).start()
    
    def username_verified(self, exists, message):
        """Handle username verification completion"""
        self.verify_button.config(state="normal")
        
        if exists:
            self.username_status.config(text=f"✓ {message}", foreground="green")
            self.add_button.config(state="normal")
            self.log_message(message, "success")
        else:
            self.username_status.config(text=f"✗ {message}", foreground="red")
            self.add_button.config(state="disabled")
            self.log_message(message, "error")
    
    def add_collaborator(self):
        """Add the verified user as collaborator to selected repositories"""
        username = self.username_entry.get().strip()
        
        # Get selected repositories
        selected_repos = [
            repo_name for repo_name, var in self.repo_vars.items() 
            if var.get()
        ]
        
        if not selected_repos:
            messagebox.showerror("Error", "Please select at least one repository")
            return
        
        if not username:
            messagebox.showerror("Error", "Please enter and verify a username")
            return
        
        # Confirm action
        result = messagebox.askyesno(
            "Confirm Action",
            f"Add '{username}' as collaborator to {len(selected_repos)} selected repositories?"
        )
        
        if not result:
            return
        
        self.log_message(f"Adding {username} as collaborator to {len(selected_repos)} repositories...")
        self.add_button.config(state="disabled")
        self.progress.start()
        
        def add_thread():
            results = self.github_client.add_collaborators_bulk(selected_repos, username)
            
            # Update UI in main thread
            self.root.after(0, self.collaborator_added, results)
        
        threading.Thread(target=add_thread, daemon=True).start()
    
    def collaborator_added(self, results):
        """Handle collaborator addition completion"""
        self.progress.stop()
        self.add_button.config(state="normal")
        
        success_count = 0
        failure_count = 0
        
        for repo_name, success, message in results:
            if success:
                success_count += 1
                self.log_message(f"✓ {repo_name}: {message}", "success")
            else:
                failure_count += 1
                self.log_message(f"✗ {repo_name}: {message}", "error")
        
        # Show summary
        summary = f"Completed: {success_count} successful, {failure_count} failed"
        self.log_message(f"\n{summary}", "info")
        
        if failure_count == 0:
            messagebox.showinfo("Success", f"Successfully added collaborator to all {success_count} repositories!")
        else:
            messagebox.showwarning(
                "Partial Success", 
                f"Added collaborator to {success_count} repositories. {failure_count} failed. Check the log for details."
            )


def main():
    """Main entry point"""
    root = tk.Tk()
    app = GitHubCollaboratorManager(root)
    
    # Center the window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()

