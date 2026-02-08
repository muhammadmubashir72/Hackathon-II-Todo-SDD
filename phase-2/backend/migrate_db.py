#!/usr/bin/env python3
"""
Migration script to update the Neon database schema with missing columns.
This script adds the new columns that were added to the Task model.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv('.env.local')  # This should load SQLite for local testing
load_dotenv('.env')        # This has the Neon database URL

# Connect to the database using the environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app_local.db")
print(f"Connecting to database: {DATABASE_URL}")

# Create engine
engine = create_engine(DATABASE_URL)

# SQL commands to add missing columns to the task table
migration_sql_commands = [
    # Add due_date column
    "ALTER TABLE task ADD COLUMN due_date TIMESTAMP;",
    # Add status column (with default value)
    "ALTER TABLE task ADD COLUMN status VARCHAR(20) DEFAULT 'todo';",
    # Add priority column (with default value)
    "ALTER TABLE task ADD COLUMN priority VARCHAR(20) DEFAULT 'medium';",
    # Add category column
    "ALTER TABLE task ADD COLUMN category VARCHAR(100);",
    # Add tags column
    "ALTER TABLE task ADD COLUMN tags VARCHAR;"
]

print("Starting migration...")
try:
    with engine.connect() as conn:
        # Check if columns exist before adding them (PostgreSQL)
        if 'postgresql' in DATABASE_URL:
            # Query to check existing columns
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'task'
            """))
            existing_columns = [row[0] for row in result.fetchall()]
            
            print(f"Existing columns in task table: {existing_columns}")
            
            # Only add columns that don't exist
            for i, sql_cmd in enumerate(migration_sql_commands):
                column_name = sql_cmd.split()[3]  # Extract column name from ALTER TABLE command
                if column_name.rstrip(';') in existing_columns:
                    print(f"Column {column_name} already exists, skipping...")
                else:
                    print(f"Adding column with command {i+1}: {sql_cmd}")
                    conn.execute(text(sql_cmd))
                    conn.commit()
        else:
            # For SQLite, just execute the commands (will fail if columns exist, which is OK for this test)
            for i, sql_cmd in enumerate(migration_sql_commands):
                print(f"Executing command {i+1}: {sql_cmd}")
                try:
                    conn.execute(text(sql_cmd))
                    conn.commit()
                    print("Command executed successfully")
                except Exception as e:
                    print(f"Command failed (might already exist): {e}")
                    
    print("Migration completed successfully!")
    
except Exception as e:
    print(f"Migration failed: {e}")
    import traceback
    traceback.print_exc()