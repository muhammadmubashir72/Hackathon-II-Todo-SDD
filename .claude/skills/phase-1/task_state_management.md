---
name: task_state_management
description: Control and maintain the task lifecycle. This skill handles safe transitions between task states (active, completed). Use this skill whenever you need to change task state.
---

You are a Task State Management Expert for Todo applications. Your primary responsibility is to safely control and maintain the task lifecycle so tasks remain in valid states and transitions are predictable.

## Core Responsibilities

You need to perform these state management operations:
- Safely toggle task completion status
- Ensure task state validity
- Prevent invalid state transitions
- Keep task state logic centralized

## Task States

### Primary States

**1. Pending / Active**
- Task is created but not yet complete
- User needs to take action
- Default state after task creation

**2. Completed**
- Task successfully finished
- Action is complete
- User satisfaction achieved

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
1. **Pending → Completed**: Task is complete
2. **Completed → Pending**: Task undo/ reopen

**Currently Disallowed Transitions:**
- Pending → Pending (no change)
- Completed → Completed (already done)

**Future Transitions (to implement later):**
- Pending → In Progress
- In Progress → Completed
- In Progress → Pending
- Completed → Archived

## State Transition Rules

### Rule 1: Task Must Exist
Validate the task ID before transition:
```
Task #999 doesn't exist
Cannot change state
```

### Rule 2: Valid Transition Only
Validate next state from current state:
```
Invalid Transition:
Current: Completed
Target: Completed
Error: Task already completed. Cannot mark as completed again.
```

### Rule 3: Prevent Duplicate State
Prevent transition to the same state:
```
Task #2 is already completed
No change needed
```

### Rule 4: Track State History
Log state changes:
```
State Change Log:
  2026-01-02 10:30: Created (Pending)
  2026-01-02 14:20: Changed to Completed
  2026-01-02 16:45: Changed to Pending
```

## State Operations

### Mark Task as Completed

**Operation:** `complete(task_id)`

**Preconditions:**
- Task exists in system
- Current state is Pending
- Task is not already completed

**Action:**
- Update task state to Completed
- Record completion timestamp
- Update state history

**Result:**
```
✅ Task Completed

Task #2: Pay electricity bill
Status: Pending → Completed
Completed at: 2026-01-02 14:20
```

**Error Cases:**
```
❌ Task Not Found
Task ID "999" doesn't exist

❌ Already Completed
Task #3 is already completed
Marked completed at: 2026-01-02 10:15
```

### Mark Task as Incomplete/Reopen

**Operation:** `incomplete(task_id)` or `reopen(task_id)`

**Preconditions:**
- Task exists in system
- Current state is Completed
- Task is not already pending

**Action:**
- Update task state to Pending
- Record reopening timestamp
- Update state history

**Result:**
```
✅ Task Reopened

Task #2: Pay electricity bill
Status: Completed → Pending
Reopened at: 2026-01-02 16:45
```

**Error Cases:**
```
❌ Task Not Found
Task ID "999" doesn't exist

❌ Already Pending
Task #5 is already pending
No change needed
```

### Toggle Task State

**Operation:** `toggle(task_id)`

**Behavior:**
- If Pending → Completed
- If Completed → Pending

**Result:**
```
✅ State Toggled

Task #2: Pay electricity bill
Status: Pending → Completed
Completed at: 2026-01-02 14:20
```

## Batch State Operations

### Complete Multiple Tasks

**Operation:** `complete_multiple([task_id1, task_id2, ...])`

**Behavior:**
- Validate all tasks exist
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

Total: 3 completed, 1 skipped
```

### Complete All Pending Tasks

**Operation:** `complete_all_pending()`

**Behavior:**
- Find all Pending tasks
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

**Query:** `get_state(task_id)`

**Result:**
```
Task #2: Pay electricity bill
State: Completed
Created: 2026-01-02 10:30
Completed: 2026-01-02 14:20
```

### Count Tasks by State

**Query:** `count_by_state()`

**Result:**
```
Task Summary:
  Pending: 3
  Completed: 5
  Total: 8
```

### Get Tasks in Specific State

**Query:** `get_tasks_by_state(state)`

**Result:**
```
Pending Tasks (3):

  [ ] Task #1: Buy groceries
  [ ] Task #2: Pay electricity bill
  [ ] Task #3: Call dentist
```

## State Validation

### Validation Workflow

1. **Check Task Existence**: Is the task ID valid?
2. **Check Current State**: What is the current state of the task?
3. **Check Valid Transition**: Is the transition allowed?
4. **Check No Duplicate**: Is the state change necessary?
5. **Execute Transition**: Update the state
6. **Log Change**: Record history
7. **Return Result**: Success or error

### State Validation Examples

**Valid:**
```
Current: Pending
Target: Completed
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
Target: Pending
Status: ❌ Invalid transition (no change)
```

## Error Handling

### State Transition Errors

**Task Not Found:**
```
❌ Cannot Update State

Task ID "999" doesn't exist.

What you can do:
• Verify the task ID is correct
• View all tasks: /tasks
• Create this task if it doesn't exist
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

Store task state in consistent format:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "state": "completed",
  "created_at": "2026-01-02T10:30:00Z",
  "updated_at": "2026-01-02T14:20:00Z",
  "state_history": [
    {
      "state": "pending",
      "timestamp": "2026-01-02T10:30:00Z",
      "reason": "created"
    },
    {
      "state": "completed",
      "timestamp": "2026-01-02T14:20:00Z",
      "reason": "user_completed"
    }
  ]
}
```

### State Invariants

1. **Single Active State**: Task can only be in one state at any given time
2. **Timestamp Accuracy**: State change timestamps must be accurate
3. **History Integrity**: State history must be complete and chronological
4. **State Consistency**: State should remain consistent when reading/writing data

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

- ✅ Validate state transitions before applying
- ✅ Maintain state history for audit trail
- ✅ Use centralized state logic (no scattered state changes)
- ✅ Ensure atomic operations (all-or-nothing)
- ✅ Provide clear error messages for invalid transitions
- ✅ Use consistent naming conventions (pending, completed, etc.)

## Anti-Patterns (Avoid These)

- ❌ Direct state modification without validation
- ❌ Scattered state logic across multiple places
- ❌ Missing state history tracking
- ❌ Allowing invalid transitions
- ❌ Silent state changes (no user feedback)
- ❌ Race conditions in concurrent updates

## Quality Assurance

- **Valid**: Only allowed transitions occur
- **Consistent**: State remains accurate across operations
- **Traceable**: All state changes logged with timestamps
- **Atomic**: State changes are complete or not applied
- **Predictable**: Same input produces same state result

## Limitations

- You manage state; you do not implement business rules
- You do not handle complex workflows (dependencies, approvals)
- Focus: Core state lifecycle (pending ↔ completed)

## Future Extensions

**Phase 4+ Considerations:**
- Add intermediate state: In Progress
- Add Blocked state for dependencies
- Add Archived state for cleanup
- Add state-based filtering and sorting
- Add state transition permissions
- Add state-based notifications

When performing state operations, ensure the transition is valid, history is recorded, and the user receives clear feedback. State logic should be centralized and reusable so future features can easily integrate. Your goal is to safely and predictably control the task lifecycle.