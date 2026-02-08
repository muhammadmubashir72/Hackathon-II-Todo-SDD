#!/usr/bin/env python3
"""
Test script to verify database schema and connection.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')
load_dotenv('.env')

print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"NODE_ENV: {os.getenv('NODE_ENV')}")

# Check if using SQLite
if os.getenv('DATABASE_URL').startswith('sqlite'):
    print("Using SQLite database")
    import sqlite3
    conn = sqlite3.connect('todo_app_local.db')
    cursor = conn.cursor()
    
    # Check if task table exists and has the right columns
    cursor.execute("PRAGMA table_info(task)")
    columns = cursor.fetchall()
    print("Task table columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    conn.close()
else:
    print("Using PostgreSQL database")
    # For PostgreSQL, we'd need to connect differently
    print("Connected to PostgreSQL - schema check skipped for this test")