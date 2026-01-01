# Feature Specification: Phase I – In-Memory Todo Console Application

**Feature Branch**: `1-todo-cli`
**Created**: 2026-01-02
**Status**: Draft
**Input**: User description: "Feature: Phase I – In-Memory Todo Console Application (Reusable Intelligence Enabled)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and View Tasks (Priority: P1)

A user wants to quickly add tasks to track their work and see all tasks organized by completion status. The user interacts with a command-line interface to create tasks with titles and optional descriptions, then view them in a clean list format.

**Why this priority**: This is the core value proposition - users must be able to create and view tasks for any other features to be useful. Without this, no task management is possible.

**Independent Test**: Can be fully tested by launching the CLI, creating multiple tasks with various titles, viewing the task list, and verifying all tasks appear correctly with unique IDs and appropriate status indicators. Delivers value immediately as a basic task tracking tool.

**Acceptance Scenarios**:

1. **Given** the CLI application is running, **When** user selects "Add task" and provides "Buy groceries" as title and "From the market" as description, **Then** a new task is created with unique ID, title "Buy groceries", description "From the market", status "Pending", and appears in the task list
2. **Given** the CLI has no tasks, **When** user selects "View tasks", **Then** user sees a clear message indicating no tasks exist and option to create first task
3. **Given** the CLI has 5 tasks (3 pending, 2 completed), **When** user selects "View tasks", **Then** user sees all tasks listed with ID, title, status, and completed tasks are visually distinct from pending tasks
4. **Given** the user is adding a task, **When** user provides empty title or only whitespace, **Then** system rejects with clear error message explaining title is required and prompts user to try again

---

### User Story 2 - Mark Tasks Complete or Incomplete (Priority: P2)

A user wants to indicate which tasks have been completed and can reopen completed tasks if needed. The user toggles task completion status to track progress and handle changes.

**Why this priority**: Task completion is the primary action users take after creating tasks. This enables tracking progress and productivity. P2 because users can get initial value from P1, but completion is essential for full task lifecycle.

**Independent Test**: Can be fully tested by creating tasks, marking them complete, viewing updated status, then reopening completed tasks and verifying state changes. Delivers value by enabling progress tracking.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists with status "Pending", **When** user selects "Mark complete" and provides ID 1, **Then** task status changes to "Completed", timestamp is recorded, and task displays as completed in task list
2. **Given** a task with ID 1 exists with status "Completed", **When** user selects "Mark complete" and provides ID 1, **Then** system indicates task is already completed with timestamp and asks if user wants to mark incomplete instead
3. **Given** a task with ID 1 exists with status "Completed", **When** user selects "Mark incomplete" and provides ID 1, **Then** task status changes to "Pending", task appears as pending in task list
4. **Given** the user attempts to mark a task complete, **When** user provides task ID 999 that doesn't exist, **Then** system displays friendly error message indicating task not found and suggests viewing all tasks to find correct ID

---

### User Story 3 - Update and Delete Tasks (Priority: P3)

A user wants to correct mistakes in task information and remove tasks that are no longer relevant. The user can modify task titles/descriptions and delete tasks completely from the list.

**Why this priority**: Users make mistakes and circumstances change. While not essential for initial use, update and delete are standard CRUD operations that users expect. P3 because basic create/read/view functionality from P1 and P2 provides immediate value.

**Independent Test**: Can be fully tested by creating tasks, updating titles/descriptions, viewing changes, then deleting tasks and verifying removal. Delivers value by enabling correction and cleanup.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 has title "Buy groceries", **When** user selects "Update task", provides ID 1, and new title "Buy groceries and milk", **Then** task title updates to "Buy groceries and milk", description remains unchanged, and updated task displays correctly
2. **Given** a task with ID 1 exists, **When** user selects "Update task", provides ID 1, and empty title, **Then** system rejects with error explaining title cannot be empty and prompts user to provide valid title
3. **Given** a task with ID 1 exists, **When** user selects "Delete task" and confirms deletion with ID 1, **Then** task is permanently removed from the task list and no longer appears in any views
4. **Given** the user attempts to delete a task, **When** user provides task ID 999 that doesn't exist, **Then** system displays friendly error message indicating task not found and suggests viewing all tasks to find correct ID
5. **Given** a task with ID 1 exists, **When** user selects "Delete task", provides ID 1, but declines confirmation, **Then** task remains unchanged and user is returned to main menu

---

### Edge Cases

- What happens when user provides non-numeric input when expecting a task ID?
- How does system handle extremely long task titles (over 200 characters)?
- What happens when user creates a task with title that is identical to an existing task title?
- How does system handle special characters or emoji in task titles and descriptions?
- What happens when user enters multiple spaces between words in title or description?
- How does system handle invalid menu selections (e.g., option 6 when only 5 options exist)?
- What happens when user provides partial or ambiguous input during task operations?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create tasks with required title and optional description
- **FR-002**: System MUST generate unique sequential task IDs automatically (1, 2, 3, etc.)
- **FR-003**: System MUST validate that task title is not empty or whitespace-only before creation
- **FR-004**: System MUST display all tasks in a list showing ID, title, and completion status
- **FR-005**: System MUST visually distinguish completed tasks from pending tasks (using symbols, formatting, or other visual indicators)
- **FR-006**: System MUST allow users to update existing task titles and descriptions
- **FR-007**: System MUST reject task updates with empty or whitespace-only titles
- **FR-008**: System MUST allow users to delete tasks by providing task ID
- **FR-009**: System MUST require confirmation before permanently deleting a task
- **FR-010**: System MUST allow users to mark pending tasks as completed
- **FR-011**: System MUST allow users to mark completed tasks as pending (reopen)
- **FR-012**: System MUST record timestamp when task is created
- **FR-013**: System MUST record timestamp when task status changes (completion or reopening)
- **FR-014**: System MUST reject invalid task IDs with clear, actionable error messages
- **FR-015**: System MUST provide clear, human-friendly error messages for all error conditions (invalid input, empty fields, non-existent tasks)
- **FR-016**: System MUST prevent marking an already completed task as completed again
- **FR-017**: System MUST prevent marking an already pending task as pending again
- **FR-018**: System MUST handle non-numeric input gracefully when expecting task ID
- **FR-019**: System MUST provide option to view all tasks as reference when user provides invalid task ID
- **FR-020**: System MUST display current task count (total, pending, completed) when viewing tasks
- **FR-021**: System MUST allow users to exit the application cleanly from main menu
- **FR-022**: System MUST display clear message when task list is empty with option to create first task
- **FR-023**: System MUST normalize whitespace in user input (trim leading/trailing, collapse multiple spaces)
- **FR-024**: System MUST validate all user input through centralized validation logic
- **FR-025**: System MUST format all output through centralized formatting logic
- **FR-026**: System MUST manage all state transitions through centralized state management logic
- **FR-027**: System MUST display all errors through centralized error handling logic
- **FR-028**: System MUST parse all user input through centralized input parsing logic

### Key Entities

**Task**: Represents a single todo item that users create, track, and complete. Contains unique identifier, descriptive title, optional detailed description, current status (Pending or Completed), creation timestamp, and status change timestamp (when applicable).

**Task List**: Collection of all tasks managed by the application. Maintains task count metrics (total, pending, completed) and provides methods to filter and display tasks by status.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task within 30 seconds from launching the application
- **SC-002**: Users can view their task list and see all tasks correctly formatted within 5 seconds of requesting
- **SC-003**: Users can mark a task as complete or reopen a completed task within 10 seconds
- **SC-004**: 100% of tasks display with correct completion status indicators (completed vs pending)
- **SC-005**: 100% of error messages are understandable to non-technical users (no jargon or stack traces)
- **SC-006**: Users can navigate through all CRUD operations (create, read, update, delete, toggle status) successfully on first attempt without documentation
- **SC-007**: All validation rules (empty titles, invalid IDs, duplicate prevention) are enforced consistently across all operations
- **SC-008**: Task IDs are assigned sequentially without gaps or duplicates
- **SC-009**: Application handles all edge cases (empty list, invalid input, non-existent tasks) without crashing or displaying technical errors
- **SC-010**: Output formatting remains consistent across all operations and views

## Assumptions

- Task IDs will be simple sequential integers starting from 1
- Title maximum length is 200 characters (reasonable for command-line display)
- Description can be any length but will be displayed in a format suitable for CLI
- User is comfortable with command-line interface and keyboard input
- Application runs in a terminal with standard character width (80+ characters)
- No concurrent users or multi-threading requirements (single-user session)
- All data is lost when application exits (no persistence requirement for Phase I)
- User input is in English (no internationalization requirements for Phase I)
- No authentication or user management required (single user session)
