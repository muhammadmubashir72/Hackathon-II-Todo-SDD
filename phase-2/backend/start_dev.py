#!/usr/bin/env python3
"""
Development startup script for the Todo API.
This script initializes the database and starts the server.
"""

import subprocess
import sys
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv('.env.local')
    load_dotenv('.env')
    
    # Print database URL for debugging (remove password for security)
    db_url = os.getenv("DATABASE_URL", "")
    if "://" in db_url:
        protocol = db_url.split("://")[0]
        rest = db_url.split("://")[1]
        if "@" in rest:
            # Mask the password in the connection string
            user_pass_host = rest.split("@")[0]
            host_part = rest.split("@")[1]
            if ":" in user_pass_host:
                user_pass = user_pass_host.split(":")[0]
                password = user_pass_host.split(":")[1]
                masked_url = f"{protocol}://{user_pass}:***@{host_part}"
            else:
                masked_url = db_url
        else:
            masked_url = db_url
    else:
        masked_url = db_url
    
    print(f"Using database: {masked_url}")
    
    # Initialize the database by importing and calling create_tables
    try:
        from src.database import create_tables
        print("Initializing database...")
        create_tables()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
    
    # Start the server
    print("Starting server...")
    port = os.getenv("PORT", "8000")  # Default to 8000 if PORT is not set
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", port])
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()