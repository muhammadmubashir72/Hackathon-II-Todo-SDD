# Operation Contracts: Phase I – In-Memory Todo Console Application

**Branch**: 1-todo-cli
**Date**: 2026-01-02
**Purpose**: Define operation contracts for all user actions

## Operation 1: Create Task

**User Action**: User selects "Add task" from menu and provides title (and optional description)

**Input**:
```json
{
    "title": "string (required, max 200 chars, not empty/whitespace)",
    "description": "string (optional)"
}
```

**Validation**:
- Title must not be empty or whitespace-only (task_validation skill)
- Title must not exceed 200 characters
- Input normalized by input_parsing skill (trim whitespace, collapse spaces)

**Output** (Success):
```json
{
    "status": "success",
    "task": {
        "id": 1,
        "title": "Buy groceries",
        "description": "From the market",
        "status": "Pending",
        "created_at": "2026-01-02T10:30:00Z",
        "updated_at": null
    },
    "message": "Task created successfully"
}
```

**Output** (Error):
```json
{
    "status": "error",
    "error_type": "invalid_title",
    "message": "Title cannot be empty. Please provide a descriptive title."
}
```

**Business Logic**:
1. Parse input using input_parsing skill
2. Validate using task_validation skill
3. Generate sequential ID (next integer)
4. Create task with status "Pending"
5. Set created_at timestamp to current time
6. Append to task list
7. Format output using task_formatting skill

---

## Operation 2: View Tasks

**User Action**: User selects "View tasks" from menu

**Input**: None

**Output** (Success - Tasks Exist):
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Your Tasks (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [✓] Task #1: Buy groceries
      Status: Completed
      Created: 2026-01-02 10:30

  [ ] Task #2: Pay electricity bill
      Status: Pending
      Created: 2026-01-02 11:00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Output** (Success - Empty List):
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  No Tasks Found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You don't have any tasks yet.
Would you like to create one? (1) Yes / (2) No

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Business Logic**:
1. Check if task list is empty
2. If empty, display empty message using task_formatting skill
3. If not empty, format all tasks using task_formatting skill
4. Completed tasks show [✓], pending tasks show [ ]
5. Display metrics (total, pending, completed)

---

## Operation 3: Update Task

**User Action**: User selects "Update task" from menu, provides task ID and updates (title and/or description)

**Input**:
```json
{
    "task_id": "int (required)",
    "title": "string (optional, max 200 chars)",
    "description": "string (optional)"
}
```

**Validation**:
- Task ID must be numeric (input_parsing skill)
- Task must exist (task_validation skill)
- If title provided, must not be empty or whitespace-only (task_validation skill)

**Output** (Success):
```json
{
    "status": "success",
    "task": {
        "id": 1,
        "title": "Buy groceries and milk",
        "description": "From the market",
        "status": "Pending",
        "created_at": "2026-01-02T10:30:00Z",
        "updated_at": "2026-01-02T12:00:00Z"
    },
    "message": "Task updated successfully"
}
```

**Output** (Error - Invalid ID):
```json
{
    "status": "error",
    "error_type": "task_not_found",
    "task_id": 999,
    "message": "Task #999 does not exist. View all tasks to find correct ID."
}
```

**Output** (Error - Empty Title):
```json
{
    "status": "error",
    "error_type": "invalid_title",
    "message": "Title cannot be empty. Please provide a descriptive title."
}
```

**Business Logic**:
1. Parse task ID using input_parsing skill
2. Validate task exists using task_validation skill
3. Validate title (if provided) using task_validation skill
4. Update task attributes (preserve unchanged values)
5. Set updated_at timestamp
6. Format output using task_formatting skill
7. Handle errors using error_handling skill

---

## Operation 4: Delete Task

**User Action**: User selects "Delete task" from menu, provides task ID, confirms deletion

**Input**:
```json
{
    "task_id": "int (required)",
    "confirmed": "boolean (required)"
}
```

**Validation**:
- Task ID must be numeric (input_parsing skill)
- Task must exist (task_validation skill)
- Confirmation must be true

**Output** (Success - Confirmed):
```json
{
    "status": "success",
    "task_id": 1,
    "message": "Task deleted successfully"
}
```

**Output** (Success - Not Confirmed):
```json
{
    "status": "cancelled",
    "task_id": 1,
    "message": "Task deletion cancelled. Task not deleted."
}
```

**Output** (Error - Invalid ID):
```json
{
    "status": "error",
    "error_type": "task_not_found",
    "task_id": 999,
    "message": "Task #999 does not exist. View all tasks to find correct ID."
}
```

**Business Logic**:
1. Parse task ID using input_parsing skill
2. Validate task exists using task_validation skill
3. Prompt for confirmation
4. If confirmed, remove task from list
5. Format output using task_formatting skill
6. Handle errors using error_handling skill

---

## Operation 5: Mark Task Complete

**User Action**: User selects "Mark complete" from menu, provides task ID

**Input**:
```json
{
    "task_id": "int (required)"
}
```

**Validation**:
- Task ID must be numeric (input_parsing skill)
- Task must exist (task_validation skill)
- Task must be in "Pending" state (task_state_management skill)

**Output** (Success):
```json
{
    "status": "success",
    "task": {
        "id": 1,
        "title": "Buy groceries",
        "description": "From the market",
        "status": "Completed",
        "created_at": "2026-01-02T10:30:00Z",
        "updated_at": "2026-01-02T14:20:00Z"
    },
    "message": "Task marked as completed"
}
```

**Output** (Error - Already Completed):
```json
{
    "status": "error",
    "error_type": "invalid_state_transition",
    "task_id": 1,
    "current_state": "Completed",
    "message": "Task #1 is already completed (completed at 2026-01-02 10:15). Would you like to mark it incomplete instead?"
}
```

**Output** (Error - Invalid ID):
```json
{
    "status": "error",
    "error_type": "task_not_found",
    "task_id": 999,
    "message": "Task #999 does not exist. View all tasks to find correct ID."
}
```

**Business Logic**:
1. Parse task ID using input_parsing skill
2. Validate task exists using task_validation skill
3. Check current state using task_state_management skill
4. If Pending, transition to Completed (valid)
5. If Completed, reject with error (invalid transition)
6. Set updated_at timestamp on state change
7. Format output using task_formatting skill
8. Handle errors using error_handling skill

---

## Operation 6: Mark Task Incomplete

**User Action**: User selects "Mark incomplete" from menu, provides task ID

**Input**:
```json
{
    "task_id": "int (required)"
}
```

**Validation**:
- Task ID must be numeric (input_parsing skill)
- Task must exist (task_validation skill)
- Task must be in "Completed" state (task_state_management skill)

**Output** (Success):
```json
{
    "status": "success",
    "task": {
        "id": 1,
        "title": "Buy groceries",
        "description": "From the market",
        "status": "Pending",
        "created_at": "2026-01-02T10:30:00Z",
        "updated_at": "2026-01-02T16:45:00Z"
    },
    "message": "Task marked as incomplete (reopened)"
}
```

**Output** (Error - Already Pending):
```json
{
    "status": "error",
    "error_type": "invalid_state_transition",
    "task_id": 2,
    "current_state": "Pending",
    "message": "Task #2 is already pending. No change needed."
}
```

**Output** (Error - Invalid ID):
```json
{
    "status": "error",
    "error_type": "task_not_found",
    "task_id": 999,
    "message": "Task #999 does not exist. View all tasks to find correct ID."
}
```

**Business Logic**:
1. Parse task ID using input_parsing skill
2. Validate task exists using task_validation skill
3. Check current state using task_state_management skill
4. If Completed, transition to Pending (valid)
5. If Pending, reject with error (invalid transition)
6. Set updated_at timestamp on state change
7. Format output using task_formatting skill
8. Handle errors using error_handling skill

---

## Operation 7: Exit Application

**User Action**: User selects "Exit" from menu

**Input**: None

**Output**:
```
Thank you for using Todo CLI!

Goodbye!
```

**Business Logic**:
1. Display farewell message
2. Exit main loop
3. Terminate application
4. Note: All data is lost (in-memory only, no persistence)

---

## Error Handling Contract

All operations follow error_handling skill contract:

**Error Message Format**:
```
❌ Error Type: [Specific Category]

[Clear explanation of what went wrong]

What you can do:
• [Actionable step 1]
• [Actionable step 2]

Need help? [Support guidance]
```

**Error Severity Levels**:
- **ℹ️ Informational**: Non-critical, suggestions
- **⚠️ Warning**: Potential issue but operation continues
- **❌ Error**: Operation failed, user action required
- **🚨 Critical**: System failure, immediate attention

**Error Recovery**:
- Suggest valid input format with examples
- Provide retry option
- Offer alternatives (view tasks, create task, etc.)
- Never display stack traces or technical jargon
