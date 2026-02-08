@echo off
REM Batch script to run the Todo CLI application

cd /d "%~dp0"

REM Activate the virtual environment created by uv
call .venv\Scripts\activate.bat

REM Run the application
python run_todo_app.py