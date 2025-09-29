#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Check database schema to verify all columns exist.
"""

from app import app, db, User, PlacementMessage

def check_database():
    """Check if database schema is correct."""
    with app.app_context():
        try:
            # Check if tables exist
            print("🔍 Checking database schema...")
            
            # Test User table
            user_columns = db.inspect(User).columns.keys()
            print(f"✅ User table columns: {user_columns}")
            
            # Test PlacementMessage table
            message_columns = db.inspect(PlacementMessage).columns.keys()
            print(f"✅ PlacementMessage table columns: {message_columns}")
            
            # Check if profile_completed column exists
            if 'profile_completed' in user_columns:
                print("✅ profile_completed column exists in User table")
            else:
                print("❌ profile_completed column missing in User table")
            
            # Test a simple query
            user_count = User.query.count()
            message_count = PlacementMessage.query.count()
            print(f"📊 Database stats: {user_count} users, {message_count} messages")
            
            print("✅ Database schema is correct!")
            
        except Exception as e:
            print(f"❌ Database error: {e}")

if __name__ == '__main__':
    check_database()

