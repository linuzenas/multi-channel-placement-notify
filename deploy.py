#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Deployment script for Placement Messenger application.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_environment_file():
    """Check if .env file exists."""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        print("   Please copy env_example.txt to .env and configure it")
        return False
    print("✅ .env file found")
    return True

def install_dependencies():
    """Install Python dependencies."""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def create_directories():
    """Create necessary directories."""
    directories = ['static/css', 'static/js', 'static/images', 'templates/admin', 'templates/student']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")
    return True

def initialize_database():
    """Initialize the database."""
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
            print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def main():
    """Main deployment function."""
    print("🚀 Starting deployment of Placement Messenger...")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_environment_file():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    print("\n🎉 Deployment completed successfully!")
    print("=" * 50)
    print("📋 Next steps:")
    print("   1. Configure your .env file with proper credentials")
    print("   2. Set up Google OAuth in Google Cloud Console")
    print("   3. Create a Telegram bot and get the token")
    print("   4. Configure Gmail app password")
    print("   5. Run: python run.py")
    print("   6. Access: http://localhost:5000")
    print("=" * 50)

if __name__ == '__main__':
    main()
