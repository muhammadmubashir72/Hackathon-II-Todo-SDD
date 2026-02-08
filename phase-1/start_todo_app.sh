#!/bin/bash
# Shell script to run the Todo CLI application

# Change to the script's directory
cd "$(dirname "$0")"

# Activate the virtual environment created by uv
source .venv/bin/activate

# Run the application
python run_todo_app.py