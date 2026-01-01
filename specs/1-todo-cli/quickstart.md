# Quickstart Guide: Phase I – In-Memory Todo Console Application

**Branch**: 1-todo-cli
**Date**: 2026-01-02
**Purpose**: Setup and testing guide for the Todo CLI application

## Prerequisites

- Python 3.13 or higher
- Linux/WSL environment
- Terminal/Command-line interface

## Installation

1. **Clone repository** (if not already done):
   ```bash
   cd /path/to/hackathon-ii-todo-sdd
   ```

2. **Checkout feature branch**:
   ```bash
   git checkout 1-todo-cli
   ```

3. **Verify Python version**:
   ```bash
   python --version
   # Output: Python 3.13.x or higher
   ```

4. **No dependencies to install**: This project uses Python standard library only.

## Running the Application

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **You should see the main menu**:
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         Todo Console Application
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Choose an option:

   1) Add task
   2) View tasks
   3) Update task
   4) Delete task
   5) Mark complete
   6) Mark incomplete
   7) Exit

   Your choice: _
   ```

## Testing Scenarios

### Test 1: Create and View Tasks (User Story 1)

**Steps**:
1. Launch application: `python main.py`
2. Select option `1` to add task
3. Enter title: `Buy groceries`
4. Enter description (optional): `From the market`
5. Verify task created with ID 1 and status Pending
6. Select option `1` again to add second task
7. Enter title: `Pay electricity bill`
8. Enter description: (leave empty)
9. Verify task created with ID 2
10. Select option `2` to view tasks
11. Verify both tasks displayed with correct IDs, titles, and status
12. Verify completed tasks show [✓] (none yet) and pending tasks show [ ]

**Expected Output**:
```
  Your Tasks (2)

  [ ] Task #1: Buy groceries
      Status: Pending
      Created: 2026-01-02 10:30

  [ ] Task #2: Pay electricity bill
      Status: Pending
      Created: 2026-01-02 11:00
```

**Acceptance**: ✅ Tasks created with unique IDs, listed with correct formatting

---

### Test 2: Mark Tasks Complete (User Story 2)

**Steps**:
1. From main menu, select option `5` (Mark complete)
2. Enter task ID: `1`
3. Verify task marked as completed with timestamp
4. Select option `2` to view tasks
5. Verify Task #1 shows [✓] (completed) and Task #2 shows [ ] (pending)
6. Select option `5` again, enter task ID: `1`
7. Verify error: "Task #1 is already completed"
8. Select option `6` (Mark incomplete)
9. Enter task ID: `1`
10. Verify task marked as pending again
11. View tasks and verify Task #1 shows [ ]

**Expected Output**:
```
✅ Task Completed

Task #1: Buy groceries
Status: Pending → Completed
Completed at: 2026-01-02 14:20
```

**Acceptance**: ✅ Task state toggles between Pending and Completed, invalid transitions blocked

---

### Test 3: Update and Delete Tasks (User Story 3)

**Steps**:
1. Create a task with title: `Test task`
2. Select option `3` (Update task)
3. Enter task ID: `1`
4. Enter new title: `Updated test task`
5. Enter new description: (leave empty)
6. Verify task updated with new title
7. Select option `3` again, enter task ID: `1`
8. Enter title: (empty)
9. Verify error: "Title cannot be empty"
10. Select option `4` (Delete task)
11. Enter task ID: `1`
12. Confirm deletion: `y`
13. Verify task deleted, no longer in list
14. Create another task, select option `4`, enter non-existent ID: `999`
15. Verify error: "Task #999 does not exist"

**Expected Output**:
```
✅ Task Updated

Task #1: Updated test task
Title changed successfully
```

```
❌ Task Not Found

Task ID "999" doesn't exist.
View all tasks to find correct ID.
```

**Acceptance**: ✅ Tasks updated and deleted with validation and error handling

---

### Test 4: Empty Task List

**Steps**:
1. Start fresh application (no tasks)
2. Select option `2` (View tasks)
3. Verify empty message displayed
4. Verify option to create first task offered

**Expected Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  No Tasks Found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You don't have any tasks yet.
Would you like to create one? (1) Yes / (2) No
```

**Acceptance**: ✅ Empty list handled gracefully with helpful guidance

---

### Test 5: Edge Cases

**Test 5a: Empty Title**
1. Select option `1` (Add task)
2. Enter title: (empty, just press Enter)
3. Verify error: "Title cannot be empty"

**Test 5b: Whitespace-Only Title**
1. Select option `1` (Add task)
2. Enter title: `   ` (only spaces)
3. Verify error: "Title cannot be empty"

**Test 5c: Non-Numeric Task ID**
1. Create a task
2. Select option `5` (Mark complete)
3. Enter task ID: `abc`
4. Verify error: "Invalid task ID: expected a number"

**Test 5d: Long Title**
1. Select option `1` (Add task)
2. Enter title: (very long, >200 characters)
3. Verify error: "Title too long" OR title truncated

**Test 5e: Special Characters**
1. Select option `1` (Add task)
2. Enter title: `Buy groceries 🛒 and milk 🥛`
3. Verify task created successfully, emoji displayed correctly

**Test 5f: Invalid Menu Selection**
1. From main menu, enter: `8`
2. Verify error: "Invalid selection, choose 1-7"

**Acceptance**: ✅ All edge cases handled gracefully without crashing

---

### Test 6: Task Count Metrics

**Steps**:
1. Create 5 tasks (Task #1 through Task #5)
2. Mark 2 tasks as complete (Task #1, Task #2)
3. Leave 3 tasks as pending (Task #3, Task #4, Task #5)
4. Select option `2` (View tasks)
5. Verify header shows: "Your Tasks (5)"
6. Verify tasks listed in order (completed first or all together)
7. Verify each task has correct status indicator

**Expected Output**:
```
  Your Tasks (5)

  [✓] Task #1: First task
      Status: Completed

  [✓] Task #2: Second task
      Status: Completed

  [ ] Task #3: Third task
      Status: Pending

  [ ] Task #4: Fourth task
      Status: Pending

  [ ] Task #5: Fifth task
      Status: Pending
```

**Acceptance**: ✅ Task count displayed correctly, all tasks listed

---

## Performance Validation

**Expected Performance** (from spec):
- Create task within 30 seconds of launch: ✅ Should be <1 second
- View tasks within 5 seconds: ✅ Should be <1 second
- Mark complete within 10 seconds: ✅ Should be <1 second

**Test**: Time each operation using stopwatch
- Add task: < 1 second
- View tasks (100 tasks): < 1 second
- Mark complete: < 1 second
- Update task: < 1 second
- Delete task: < 1 second

---

## Error Message Validation

Verify all error messages are:
- Human-friendly (no jargon)
- Actionable (tell user what to do)
- Consistent in tone and format
- Helpful (suggest alternatives)

**Check List**:
- [ ] Empty title error
- [ ] Invalid task ID error
- [ ] Task not found error
- [ ] Already completed error
- [ ] Already pending error
- [ ] Invalid menu selection error
- [ ] Non-numeric input error

---

## Reusable Skills Validation

Verify all operations use defined skills:
- [ ] `task_validation` - All task operations validated before execution
- [ ] `input_parsing` - All user input normalized (trimmed, converted)
- [ ] `task_formatting` - All output follows consistent format
- [ ] `error_handling` - All errors follow standard format with tone
- [ ] `task_state_management` - All state transitions validated

**Validation Method**:
1. Review source code (src/modules/)
2. Ensure no inline validation/parsing/formatting logic
3. Ensure all operations delegate to skill modules/functions

---

## Cleanup

To reset testing state:
1. Exit application
2. All data is lost automatically (in-memory only)
3. Relaunch application: `python main.py`
4. Start fresh with empty task list

---

## Troubleshooting

**Issue**: "Python command not found"
**Solution**: Install Python 3.13+ or add to PATH

**Issue**: "Invalid syntax" or module errors
**Solution**: Verify Python version >= 3.13

**Issue**: Tasks disappear after closing application
**Expected**: This is Phase I behavior (in-memory only, no persistence)

**Issue**: Application crashes on invalid input
**Solution**: Report bug - all invalid input should be handled gracefully

---

## Success Criteria Checklist

- [ ] SC-001: Task creation within 30 seconds ✅
- [ ] SC-002: Task list view within 5 seconds ✅
- [ ] SC-003: Mark complete within 10 seconds ✅
- [ ] SC-004: 100% correct status indicators
- [ ] SC-005: 100% understandable error messages
- [ ] SC-006: First-attempt success for all operations
- [ ] SC-007: All validation rules enforced consistently
- [ ] SC-008: Task IDs sequential without gaps
- [ ] SC-009: All edge cases handled without crashing
- [ ] SC-010: Output formatting consistent across views

All tests should pass before proceeding to Phase II.
