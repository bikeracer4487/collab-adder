#!/usr/bin/env python3
"""
GitHub Collaborator Manager
Main entry point for the application

Usage: python3 main.py
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import requests
        return True, None
    except ImportError as e:
        return False, str(e)

def main():
    """Main entry point with error handling"""
    try:
        # Check dependencies
        deps_ok, error = check_dependencies()
        if not deps_ok:
            # Create a simple error dialog
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            messagebox.showerror(
                "Missing Dependencies",
                f"Required dependency missing: {error}\n\n"
                "Please install required packages:\n"
                "pip3 install requests\n\n"
                "Or run: pip3 install -r requirements.txt"
            )
            return 1
        
        # Import and run the main application
        from main_app import main as run_app
        run_app()
        return 0
        
    except Exception as e:
        # Create a simple error dialog
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        messagebox.showerror(
            "Application Error",
            f"An error occurred while starting the application:\n\n{str(e)}\n\n"
            "Please check that all files are present and try again."
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())

