# Quick Start Guide for Todo CLI Application - Phase 1

## Running the Application

### On Windows:
Double-click `start_todo_app.bat` or run:
```
.\start_todo_app.bat
```

Alternatively, you can run directly with uv:
```
uv run python run_todo_app.py
```

### On Linux/Mac:
Make the script executable and run:
```
chmod +x start_todo_app.sh
./start_todo_app.sh
```

Alternatively, you can run directly with uv:
```
uv run python run_todo_app.py
```

## Features

Once running, the application provides these options:

1. **Add task** - Create new todo items
2. **View tasks** - See all your tasks with status
3. **Update task** - Modify existing tasks
4. **Delete task** - Remove tasks from your list
5. **Mark complete** - Mark tasks as completed
6. **Mark incomplete** - Reopen completed tasks
7. **Exit** - Quit the application

## Development

To install development dependencies:
```
uv sync
```

To run with development dependencies:
```
uv run --with pytest,black,flake8 python run_todo_app.py
```

## Project Structure

- `main.py` - Original entry point
- `run_todo_app.py` - Fixed entry point with encoding support
- `src/` - Source code for the application
- `specs/` - Specification documents
- `pyproject.toml` - Project metadata and dependencies
- `README.md` - Project documentation
- `CLI-Todo-Phase-1.mp4` - Demo video