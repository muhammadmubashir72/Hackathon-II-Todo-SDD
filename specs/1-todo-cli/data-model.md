# Data Model: Phase I – In-Memory Todo Console Application

**Branch**: 1-todo-cli
**Date**: 2026-01-02
**Purpose**: Define core data structures and entity relationships

## Core Entities

### Task

**Purpose**: Represents a single todo item that users create, track, and complete.

**Attributes**:
| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `int` | Yes | Unique sequential identifier (1, 2, 3, ...) |
| `title` | `str` | Yes | Descriptive task title (max 200 characters) |
| `description` | `str` | No | Optional detailed description |
| `status` | `str` | Yes | Task state: "Pending" or "Completed" |
| `created_at` | `str` | Yes | Timestamp when task was created (ISO 8601 format) |
| `updated_at` | `str` | No | Timestamp when task status changed (ISO 8601 format) |

**Validation Rules**:
- `id` must be positive integer (>0)
- `title` must not be empty or whitespace-only after trimming
- `title` must not exceed 200 characters
- `status` must be either "Pending" or "Completed"
- `created_at` must be valid ISO 8601 timestamp
- `updated_at` must be valid ISO 8601 timestamp if present

**State Transitions**:
```
Pending ──→ Completed (mark complete)
   ↑            ↓
   └────────────┘ (reopen)
```

**Valid Transitions**:
- Pending → Completed: User marks task as done
- Completed → Pending: User reopens task

**Invalid Transitions**:
- Pending → Pending: No state change
- Completed → Completed: Already completed

**Example**:
```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "From the market",
    "status": "Pending",
    "created_at": "2026-01-02T10:30:00Z",
    "updated_at": null
}
```

### Task List

**Purpose**: Collection of all tasks managed by the application.

**Structure**: Python `list` containing Task objects (represented as `dict`).

**Operations**:
- `add(task)`: Append new task to list
- `get_by_id(task_id)`: Retrieve task by sequential index (task_id - 1)
- `update(task_id, updates)`: Update task attributes
- `delete(task_id)`: Remove task from list
- `list_all()`: Return all tasks
- `count_by_status()`: Return metrics (total, pending, completed)

**Metrics**:
| Metric | Type | Description |
|--------|------|-------------|
| `total` | `int` | Total number of tasks in list |
| `pending` | `int` | Number of tasks with status "Pending" |
| `completed` | `int` | Number of tasks with status "Completed" |

**Example**:
```python
tasks = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "From the market",
        "status": "Completed",
        "created_at": "2026-01-02T10:30:00Z",
        "updated_at": "2026-01-02T14:20:00Z"
    },
    {
        "id": 2,
        "title": "Pay electricity bill",
        "description": "",
        "status": "Pending",
        "created_at": "2026-01-02T11:00:00Z",
        "updated_at": null
    }
]

metrics = {
    "total": 2,
    "pending": 1,
    "completed": 1
}
```

## Entity Relationships

**Relationships**: No entity relationships in Phase I. Tasks are independent (no dependencies, categories, or user associations).

**Future Extensions** (for reference):
- Task dependencies: Task A must complete before Task B
- Task categories: Tasks belong to categories (Work, Personal, Shopping)
- Task tags: Tasks have multiple tags (urgent, low-priority)
- Task due dates: Tasks have optional due dates for scheduling

## Invariants

1. **ID Uniqueness**: No two tasks have the same `id`
2. **ID Sequencing**: `id` values are sequential without gaps (1, 2, 3, ...)
3. **Status Validity**: All tasks have valid status ("Pending" or "Completed")
4. **Title Validity**: All tasks have non-empty titles
5. **Timestamp Accuracy**: Timestamps are valid ISO 8601 format strings

## Storage Model

**Type**: In-memory Python list

**Scope**: Single application session (lost on exit)

**Access Pattern**:
- Tasks stored in order of creation
- Task ID corresponds to list index position + 1
- Linear search for filtering by status
- Direct index access for lookup by ID

**Memory Constraints**:
- Assuming <1000 tasks per session (reasonable CLI usage)
- Each task ~500 bytes (dict overhead + strings)
- Total memory: <500KB per session (negligible)

## Data Integrity

**Validation Layers**:
1. **Input Validation**: `task_validation` skill validates before creation/updates
2. **Input Parsing**: `input_parsing` skill normalizes raw user input
3. **State Management**: `task_state_management` skill enforces valid transitions
4. **Error Handling**: `error_handling` skill provides graceful failure

**Error Handling**:
- Invalid ID → Task not found error
- Empty title → Validation error
- Invalid status → State transition error
- Non-existent task → Lookup error
- Malformed input → Parse error
