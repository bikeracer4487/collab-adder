#!/bin/bash
# GitHub Collaborator Manager - Quick Start Script for macOS
# This script sets up and runs the GitHub Collaborator Manager

set -e  # Exit on any error

echo "🚀 GitHub Collaborator Manager - Quick Start"
echo "============================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    echo "   You can download it from: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Please run this script from the github_collaborator_manager directory"
    echo "   The main.py file should be in the current directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
if pip3 install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "   Please try manually: pip3 install requests"
    exit 1
fi

# Test tkinter availability
echo "🔍 Checking GUI support..."
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✅ GUI support available"
else
    echo "❌ tkinter not available. On macOS, this usually means:"
    echo "   1. You're using a Python version without tkinter"
    echo "   2. Try installing Python from python.org instead of Homebrew"
    echo "   3. Or install tkinter: brew install python-tk"
    exit 1
fi

# Run the application
echo "🎯 Starting GitHub Collaborator Manager..."
echo ""
echo "📝 Quick Setup Reminder:"
echo "   1. Get your GitHub Personal Access Token from:"
echo "      https://github.com/settings/tokens"
echo "   2. Make sure it has 'repo' scope permissions"
echo "   3. Paste it in the application when prompted"
echo ""
echo "🔒 Security Note: Your token is only stored in memory while the app runs"
echo ""

# Launch the application
python3 main.py

