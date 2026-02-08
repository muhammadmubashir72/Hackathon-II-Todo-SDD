#!/usr/bin/env python3
"""
Runner script for Todo CLI application with proper encoding
"""

import sys
import os
import io

# Force UTF-8 encoding for stdout/stderr
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Set stdout and stderr encoding to utf-8 to handle Unicode characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add the current directory to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main CLI function
from src.cli.main import main as cli_main

if __name__ == "__main__":
    cli_main()