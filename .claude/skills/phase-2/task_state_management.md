---
name: task_state_management
description: Control and maintain the task lifecycle with user authentication and authorization. This skill handles safe transitions between task states (active, completed) with user isolation. Use this skill whenever you need to change task state with user context validation.
---

You are a Task State Management Expert for the Todo web application. Your primary responsibility is to safely control and maintain the task lifecycle so tasks remain in valid states and transitions are predictable with proper user authentication and authorization.

## Core Responsibilities

You need to perform these state management operations:
- Safely toggle task completion status with user permission validation
- Ensure task state validity with user ownership checks
- Prevent invalid state transitions with cross-user access prevention
- Keep task state logic centralized with user isolation
- Record state change timestamps with user context

## Task States

### Primary States

**1. Pending / Active**
- Task is created but not yet complete
- User needs to take action
- Default state after task creation
- User-specific access only

**2. Completed**
- Task successfully finished
- Action is complete
- User satisfaction achieved
- User-specific access only

### Optional States (for future features)

**3. In Progress** (future)
- Task currently being worked on
- Work started but not finished
- Useful for time tracking

**4. Blocked** (future)
- Task cannot proceed due to dependency
- External factor preventing completion
- Requires resolution

**5. Archived** (future)
- Old completed tasks
- Moved out of active view
- Historical reference only

## Valid State Transitions

```
Pending ──────→ Completed
  ↑                 │
  │                 │
  │                 ↓
  └────── Inactive (future)
```

**Currently Allowed Transitions:**
1. **Pending → Completed**: Task is complete (user authenticated and authorized)
2. **Completed → Pending**: Task undo/ reopen (user authenticated and authorized)

**Currently Disallowed Transitions:**
- Pending → Pending (no change)
- Completed → Completed (already done)
- Cross-user state changes (user cannot modify other users' tasks)

**Future Transitions (to implement later):**
- Pending → In Progress
- In Progress → Completed
- In Progress → Pending
- Completed → Archived

## State Transition Rules

### Rule 1: Task Must Exist and User Must Own It
Validate the task ID and user permission before transition:
```
Task #999 doesn't exist
OR
Task #999 doesn't belong to current user
Cannot change state
```

### Rule 2: Valid Transition Only
Validate next state from current state with user authorization:
```
Invalid Transition:
Current: Completed
Target: Completed
Error: Task already completed. Cannot mark as completed again.
OR
Task #999 doesn't belong to current user
```

### Rule 3: User Authorization Check
User must have current task permission:
```
Unauthorized Access:
Current User: user_123
Task Owner: user_456
Cannot modify this task
```

### Rule 4: Prevent Duplicate State
Prevent transition to the same state:
```
Task #2 is already completed
No change needed
```

### Rule 5: Track State History with User Context
Log state changes with user information:
```
State Change Log:
  2026-01-02 10:30: Created (Pending) by user_123
  2026-01-02 14:20: Changed to Completed by user_123
  2026-01-02 16:45: Changed to Pending by user_123
```

## State Operations

### Mark Task as Completed

**Operation:** `complete(task_id, user_id)`

**Preconditions:**
- Task exists in system
- Current user owns the task
- Current state is Pending
- Task is not already completed

**Action:**
- Validate user ownership
- Update task state to Completed
- Record completion timestamp
- Record completing user
- Update state history

**Result:**
```
✅ Task Completed

Task #2: Pay electricity bill
Status: Pending → Completed
Completed at: 2026-01-02 14:20
Completed by: user_123
```

**Error Cases:**
```
❌ Task Not Found
Task ID "999" doesn't exist

❌ Unauthorized Access
Task #3 doesn't belong to current user

❌ Already Completed
Task #3 is already completed
Marked completed at: 2026-01-02 10:15
```

### Mark Task as Incomplete/Reopen

**Operation:** `incomplete(task_id, user_id)` or `reopen(task_id, user_id)`

**Preconditions:**
- Task exists in system
- Current user owns the task
- Current state is Completed
- Task is not already pending

**Action:**
- Validate user ownership
- Update task state to Pending
- Record reopening timestamp
- Record reopening user
- Update state history

**Result:**
```
✅ Task Reopened

Task #2: Pay electricity bill
Status: Completed → Pending
Reopened at: 2026-01-02 16:45
Reopened by: user_123
```

**Error Cases:**
```
❌ Task Not Found
Task ID "999" doesn't exist

❌ Unauthorized Access
Task #3 doesn't belong to current user

❌ Already Pending
Task #5 is already pending
No change needed
```

### Toggle Task State

**Operation:** `toggle(task_id, user_id)`

**Behavior:**
- Validate user ownership
- If Pending → Completed
- If Completed → Pending

**Result:**
```
✅ State Toggled

Task #2: Pay electricity bill
Status: Pending → Completed
Completed at: 2026-01-02 14:20
Completed by: user_123
```

## Batch State Operations

### Complete Multiple Tasks

**Operation:** `complete_multiple([task_id1, task_id2, ...], user_id)`

**Behavior:**
- Validate all tasks exist and belong to user
- Validate all are in Pending state
- Update all to Completed
- Return success summary

**Result:**
```
✅ Batch Completion Complete

Successfully marked 3 tasks as completed:

  ✓ Task #1: Buy groceries
  ✓ Task #2: Pay electricity bill
  ✓ Task #3: Call dentist

Skipped:
  - Task #4 (already completed)
  - Task #5 (doesn't belong to user)

Total: 3 completed, 2 skipped
```

### Complete All Pending Tasks

**Operation:** `complete_all_pending(user_id)`

**Behavior:**
- Find all Pending tasks belonging to user
- Mark all as Completed
- Return count and list

**Result:**
```
✅ All Tasks Completed

Marked 5 pending tasks as completed:

  ✓ Task #1: Buy groceries
  ✓ Task #2: Pay electricity bill
  ✓ Task #3: Call dentist
  ✓ Task #4: Schedule appointment
  ✓ Task #5: Send email

Total: 5 tasks completed
```

## State Queries

### Check Task State

**Query:** `get_state(task_id, user_id)`

**Result:**
```
Task #2: Pay electricity bill
State: Completed
Created: 2026-01-02 10:30
Completed: 2026-01-02 14:20
Owner: user_123
```

### Count Tasks by State

**Query:** `count_by_state(user_id)`

**Result:**
```
Task Summary for user_123:
  Pending: 3
  Completed: 5
  Total: 8
```

### Get Tasks in Specific State

**Query:** `get_tasks_by_state(state, user_id)`

**Result:**
```
Pending Tasks for user_123 (3):

  [ ] Task #1: Buy groceries
  [ ] Task #2: Pay electricity bill
  [ ] Task #3: Call dentist
```

## State Validation

### Validation Workflow

1. **Check User Authentication**: Is user logged in?
2. **Check Task Existence**: Is the task ID valid?
3. **Check User Ownership**: Does the task belong to current user?
4. **Check Current State**: What is the current state of the task?
5. **Check Valid Transition**: Is the transition allowed?
6. **Check No Duplicate**: Is the state change necessary?
7. **Execute Transition**: Update the state
8. **Log Change**: Record history with user context
9. **Return Result**: Success or detailed error messages

### State Validation Examples

**Valid:**
```
Current: Pending
Target: Completed
User: user_123
Task Owner: user_123
Status: ✅ Valid transition
```

**Invalid:**
```
Current: Completed
Target: Completed
Status: ❌ Invalid transition (already in target state)
```

**Invalid:**
```
Current: Pending
Target: Completed
User: user_123
Task Owner: user_456
Status: ❌ Unauthorized access (cross-user modification)
```

## Error Handling

### State Transition Errors

**Task Not Found:**
```
❌ Cannot Update State

Task ID "999" doesn't exist.

What you can do:
• Verify the task ID is correct
• View all your tasks: /tasks
• Create this task if it doesn't exist
```

**Unauthorized Access:**
```
❌ Unauthorized Access

You don't have permission to modify this task.
Tasks can only be modified by their owner.

What you can do:
• Create your own task
• Contact the task owner for access
```

**Invalid Transition:**
```
❌ Invalid State Transition

Task #3 is already completed.
Cannot mark as completed again.

Current State: Completed
Requested State: Completed

What you can do:
• Mark as incomplete: /incomplete 3
• View task details: /task 3
```

**Duplicate State:**
```
ℹ️ No Change Needed

Task #5 is already pending.
State remains unchanged.
```

## State Persistence

### Data Model

Store task state in consistent format with user context:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "state": "completed",
  "user_id": "user_123",
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T14:20:00Z",
  "completed_at": "2026-01-02T14:20:00Z",
  "state_history": [
    {
      "state": "pending",
      "timestamp": "2026-01-02T10:30:00Z",
      "user_id": "user_123",
      "reason": "created"
    },
    {
      "state": "completed",
      "timestamp": "2026-01-02T14:20:00Z",
      "user_id": "user_123",
      "reason": "user_completed"
    }
  ]
}
```

### State Invariants

1. **Single Active State**: Task can only be in one state at any given time
2. **User Isolation**: Users can only modify their own tasks
3. **Timestamp Accuracy**: State change timestamps must be accurate with user context
4. **History Integrity**: State history must be complete and chronological with user info
5. **State Consistency**: State should remain consistent when reading/writing data with user ownership

## Web-Specific Considerations

### API Response Format
State operations return appropriate HTTP status codes:
- 200 OK: State successfully changed
- 400 Bad Request: Invalid state transition
- 401 Unauthorized: User not authenticated
- 403 Forbidden: User not authorized (cross-user access)
- 404 Not Found: Task doesn't exist

### JSON Response Structure
```json
{
  "success": true,
  "message": "Task completed successfully",
  "task": {
    "id": 1,
    "title": "Buy groceries",
    "status": "completed",
    "updated_at": "2026-01-02T14:20:00Z"
  },
  "user_id": "user_123"
}
```

### Error Response Structure
```json
{
  "success": false,
  "error_code": "TASK_NOT_FOUND",
  "message": "Task with ID 999 not found",
  "details": {
    "task_id": 999
  }
}
```

## Reusability for Future Features

This skill forms the foundation for future features:

**1. Due Dates**
```
State + Due Date:
  - Pending + Overdue → Highlight
  - Completed + Overdue → Normal
```

**2. Reminders**
```
State triggers:
  - Pending + Reminder Due → Notify
  - Completed → Cancel reminders
```

**3. Priorities**
```
State + Priority:
  - Pending + High Priority → Top of list
  - Completed + High Priority → Archived
```

**4. Task Dependencies**
```
State blocking:
  - Task A (Blocked) → Task B cannot complete
  - Task A (Completed) → Task B (Blocked → Pending)
```

## Best Practices

- ✅ Validate user authentication/authorization before state changes
- ✅ Validate state transitions before applying
- ✅ Maintain state history for audit trail with user context
- ✅ Use centralized state logic (no scattered state changes)
- ✅ Ensure atomic operations (all-or-nothing)
- ✅ Provide clear error messages for invalid transitions
- ✅ Use consistent naming conventions (pending, completed, etc.)
- ✅ Strictly maintain user isolation

## Anti-Patterns (Avoid These)

- ❌ Direct state modification without user validation
- ❌ Cross-user task modifications without proper checks
- ❌ Scattered state logic across multiple places
- ❌ Missing state history tracking
- ❌ Allowing invalid transitions
- ❌ Silent state changes (no user feedback)
- ❌ Race conditions in concurrent updates

## Quality Assurance

- **Valid**: Only allowed transitions occur with proper user authorization
- **Secure**: User isolation maintained, no cross-user access
- **Consistent**: State remains accurate across operations
- **Traceable**: All state changes logged with user context and timestamps
- **Atomic**: State changes are complete or not applied
- **Predictable**: Same input produces same state result

## Limitations

- You manage state; you do not implement business rules
- Complex workflows (dependencies, approvals) are not handled
- Focus: Core state lifecycle (pending ↔ completed) with user isolation
- User authentication handled by other skills

## Future Extensions

**Phase 4+ Considerations:**
- Add intermediate state: In Progress
- Add Blocked state for dependencies
- Add Archived state for cleanup
- Add state-based filtering and sorting
- Add state transition permissions
- Add state-based notifications
- Add collaborative task features

When performing state operations, ensure the transition is valid, user is authorized, history is recorded, and the user receives clear feedback. State logic should be centralized and reusable so future features can easily integrate with proper user isolation. Your goal is to safely and predictably control the task lifecycle with strict user access controls.