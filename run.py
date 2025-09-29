#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Placement Messenger - Startup Script

This script initializes and runs the Placement Messenger admin application.
"""

import os
import sys
from app import app, db

def check_environment():
    """Check if required environment variables are set."""
    required_vars = [
        'SECRET_KEY',
        'GMAIL_USER',
        'GMAIL_APP_PASSWORD',
        'TELEGRAM_TOKEN'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        return False
    
    print("✅ Environment variables check passed")
    return True

def check_optional_config():
    """Check optional configuration."""
    optional_vars = {
        'TELEGRAM_GROUP_ID': 'Telegram group messaging will be disabled'
    }
    
    for var, message in optional_vars.items():
        if not os.getenv(var):
            print(f"⚠️  {var} not set: {message}")

def main():
    """Main function to run the application."""
    print("🚀 Starting Placement Messenger Admin Panel...")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check optional configuration
    check_optional_config()
    
    # Initialize database
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    print("\n🌐 Application is ready!")
    print("📍 Access the application at: http://localhost:5000")
    print("📋 Features available:")
    print("   - Admin: Create and send placement messages")
    print("   - Student: View opportunities and career guidance")
    print("   - Multi-channel notifications (Email + Telegram)")
    print("=" * 50)
    
    # Run the application
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )

if __name__ == '__main__':
    main()