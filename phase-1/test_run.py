#!/usr/bin/env python3
"""
Test runner for Todo CLI application
"""

import threading
import sys
import os

# Add the current directory to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_app():
    from src.cli.main import main as cli_main
    cli_main()

if __name__ == "__main__":
    # Run the application in a thread
    app_thread = threading.Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()
    
    # Wait for a few seconds then exit
    app_thread.join(timeout=5)
    
    if app_thread.is_alive():
        print("\nApplication is running. Press Ctrl+C to exit.")
        try:
            app_thread.join()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)