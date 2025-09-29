#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify Placement Messenger setup.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🔄 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import openpyxl
        print("✅ OpenPyXL imported successfully")
    except ImportError as e:
        print(f"❌ OpenPyXL import failed: {e}")
        return False
    
    try:
        import telegram
        print("✅ python-telegram-bot imported successfully")
    except ImportError as e:
        print(f"❌ python-telegram-bot import failed: {e}")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_files():
    """Test if all required files exist."""
    print("🔄 Testing file structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'run.py',
        'requirements.txt',
        'README.md',
        'templates/base.html',
        'templates/index.html',
        'templates/admin/dashboard.html',
        'templates/admin/create_message.html',
        'templates/admin/upload_students.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files exist")
    return True

def test_environment():
    """Test environment configuration."""
    print("🔄 Testing environment configuration...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
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
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("   Please check your .env file")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_app_creation():
    """Test if the Flask app can be created."""
    print("🔄 Testing Flask app creation...")
    
    try:
        from app import app
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def test_excel_processing():
    """Test Excel file processing functionality."""
    print("🔄 Testing Excel processing...")
    
    try:
        import pandas as pd
        import tempfile
        import os
        
        # Create test data
        test_data = {
            'name': ['John Doe', 'Jane Smith'],
            'email': ['john@klu.ac.in', 'jane@klu.ac.in']
        }
        
        # Create temporary Excel file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_file.close()  # Close the file handle
            
            df = pd.DataFrame(test_data)
            df.to_excel(tmp_file.name, index=False)
            
            # Test reading the file
            df_read = pd.read_excel(tmp_file.name)
            
            # Clean up
            try:
                os.unlink(tmp_file.name)
            except:
                pass  # Ignore cleanup errors
            
            if len(df_read) == 2 and 'name' in df_read.columns and 'email' in df_read.columns:
                print("✅ Excel processing works correctly")
                return True
            else:
                print("❌ Excel processing failed - data mismatch")
                return False
                
    except Exception as e:
        print(f"❌ Excel processing failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Testing Placement Messenger Admin Setup...")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_files),
        ("Python Imports", test_imports),
        ("Environment Config", test_environment),
        ("Flask App Creation", test_app_creation),
        ("Excel Processing", test_excel_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Setup is ready.")
        print("\n📋 Next steps:")
        print("   1. Configure your .env file")
        print("   2. Set up Gmail app password")
        print("   3. Create Telegram bot and get group ID")
        print("   4. Run: python run.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()