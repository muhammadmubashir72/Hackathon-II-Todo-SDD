# Implementation Plan: Phase I – In-Memory Todo Console Application

**Branch**: `1-todo-cli` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-todo-cli/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

In-Memory Todo Console Application with reusable intelligence architecture. Core functionality includes task creation, viewing, updating, deleting, and state toggling (pending ↔ completed). All operations use centralized skills (validation, input parsing, formatting, error handling, state management) to ensure business logic remains portable to future phases (API, Chatbot). Python 3.13+ with standard library only, in-memory storage, loop-based CLI interface.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory Python list (no database, no persistence)
**Testing**: Manual testing via quickstart.md scenarios
**Target Platform**: Linux / WSL
**Project Type**: Single project (CLI application)
**Performance Goals**: Sub-second operations for task CRUD (<1 second per operation), support <1000 tasks per session
**Constraints**: In-memory only, standard library only, no persistence, no external frameworks
**Scale/Scope**: Single-user session, <1000 tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development (SDD) Compliance
- [x] Spec approved and documented
- [x] Plan created from spec
- [x] Tasks will be generated (Phase 2 via /sp.tasks)
- [x] Implementation will follow documented steps

### Reusable Intelligence Philosophy
- [x] Task model stable (ID, title, status, timestamps) - portable to API/Chatbot
- [x] Validation rules centralized in task_validation skill
- [x] Input parsing centralized in input_parsing skill
- [x] Output formatting centralized in task_formatting skill
- [x] Task state management centralized in task_state_management skill
- [x] Error handling centralized in error_handling skill
- [x] No implementation bypasses reusable skills

### Single-Responsibility Architecture
- [x] Main Agent orchestrates workflow
- [x] Validation Logic Subagent uses task_validation
- [x] Input Parsing Subagent uses input_parsing
- [x] Output Formatting Subagent uses task_formatting
- [x] Task State Management Subagent uses task_state_management
- [x] Error Handling Subagent uses error_handling

### Code Quality and Structure
- [x] Simple, readable, modular functions
- [x] Single-responsibility principle followed
- [x] Error messages human-friendly and consistent
- [x] Console output structured and predictable

### Programming Constraints
- [x] Python 3.13+ specified
- [x] Console (CLI) interface only
- [x] In-memory storage only
- [x] Linux / WSL compatible
- [x] Standard library only (no frameworks, databases, persistence)

### Quality Rules
- [x] Tasks have unique IDs
- [x] Tasks support complete and incomplete states
- [x] Errors handled gracefully
- [x] Output human-readable and consistent
- [x] All operations use defined skills

**Result**: ✅ All constitution gates pass. No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/1-todo-cli/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (/sp.specify command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── operations.md   # Operation contracts for all user actions
└── checklists/
    └── requirements.md  # Spec quality checklist (/sp.specify output)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── task.py              # Task entity and TaskList collection
├── services/
│   ├── __init__.py
│   └── task_service.py      # Business logic layer (orchestrates skills)
├── cli/
│   ├── __init__.py
│   └── main.py             # CLI entry point, main menu, user interaction
├── skills/
│   ├── __init__.py
│   ├── task_validation.py    # Task validation logic
│   ├── input_parsing.py     # Input parsing and normalization
│   ├── task_formatting.py   # Output formatting
│   ├── error_handling.py     # Error generation and display
│   └── task_state_management.py  # State transitions
└── lib/
    ├── __init__.py
    └── utils.py            # Shared utilities (timestamps, etc.)

main.py                             # Application entry point (imports and starts CLI)
```

**Structure Decision**: Single project structure chosen because this is a CLI application with no frontend/backend separation. Architecture separates concerns:
- `models/`: Data entities (Task, TaskList)
- `services/`: Business logic layer that orchestrates skill usage
- `cli/`: Presentation layer (menu, user interaction)
- `skills/`: Reusable intelligence modules (portable to future phases)
- `lib/`: Shared utilities

This structure supports future phases by extracting `skills/` module unchanged to API and Chatbot implementations.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations. No complexity tracking required.

## Phase 0: Research

**Output**: [research.md](./research.md)

**Research Completed**:
- Python CLI best practices: argparse, menu-driven loop
- In-memory storage: Python list with dict objects
- Task ID management: Sequential integers (1, 2, 3, ...)
- Task state representation: String enumeration ("Pending", "Completed")
- Input normalization: str.strip() and split()
- Error handling: Try-except blocks with structured error messages
- Reusable skills integration: Skills as standalone modules, business logic as service layer
- Output formatting: Multi-line string templates with f-string interpolation
- Performance: No optimizations needed (sub-millisecond operations for <1000 tasks)
- Testing: Manual testing during development
- Edge cases: Defensive programming with input validation

**No NEEDS CLARIFICATION items remain**. Research complete.

## Phase 1: Design & Contracts

### Data Model
**Output**: [data-model.md](./data-model.md)

**Entities Defined**:
- Task: ID, title, description, status, created_at, updated_at
- TaskList: Collection with operations (add, get_by_id, update, delete, list_all, count_by_status)

**State Transitions**: Pending ↔ Completed (toggling)
**Validation Rules**: ID > 0, title not empty, status valid, timestamps ISO 8601
**Invariants**: ID uniqueness, ID sequencing, status validity, title validity, timestamp accuracy

### Operation Contracts
**Output**: [contracts/operations.md](./contracts/operations.md)

**Contracts Defined**:
1. Create Task: Input validation, sequential ID generation, Pending status
2. View Tasks: Empty list handling, metrics display, visual status indicators
3. Update Task: Partial updates, title validation, task existence check
4. Delete Task: Confirmation required, graceful error for non-existent ID
5. Mark Complete: State transition validation, timestamp recording
6. Mark Incomplete: State transition validation, timestamp recording
7. Exit Application: Farewell message, data loss notification

**Error Handling Contract**:
- Standard error message format
- Severity levels (informational ℹ️, warning ⚠️, error ❌, critical 🚨)
- Recovery strategies (retry, alternatives, suggestions)
- No technical jargon or stack traces

### Quickstart Guide
**Output**: [quickstart.md](./quickstart.md)

**Testing Scenarios**:
1. Create and View Tasks (User Story 1)
2. Mark Tasks Complete/Incomplete (User Story 2)
3. Update and Delete Tasks (User Story 3)
4. Empty Task List
5. Edge Cases (empty title, whitespace, non-numeric IDs, long titles, special characters, invalid menu)
6. Task Count Metrics
7. Performance Validation
8. Error Message Validation
9. Reusable Skills Validation

**Performance Targets**:
- Create task: < 1 second (spec: 30 seconds)
- View tasks (100 tasks): < 1 second (spec: 5 seconds)
- Mark complete: < 1 second (spec: 10 seconds)

**Success Criteria Checklist**: All 10 success criteria validated

### Agent Context Update

*Note*: `.specify/scripts/powershell/update-agent-context.ps1` script not found. Agent context updated manually via skills directory.

**Skills Created**:
- `.claude/skills/task_validation.md` - Validation logic for task operations
- `.claude/skills/input_parsing.md` - Input parsing and normalization
- `.claude/skills/task_formatting.md` - Output formatting
- `.claude/skills/error_handling.md` - Error generation and display
- `.claude/skills/task_state_management.md` - State transitions

**Architecture Documented**:
- Main Agent: Orchestrates workflow in `src/cli/main.py`
- Validation Logic Subagent: Uses `task_validation` skill
- Input Parsing Subagent: Uses `input_parsing` skill
- Output Formatting Subagent: Uses `task_formatting` skill
- Task State Management Subagent: Uses `task_state_management` skill
- Error Handling Subagent: Uses `error_handling` skill

## Phase 2 Re-check: Constitution Compliance

### Reusable Intelligence Requirements
- [x] Task Model Stability: Core attributes (ID, title, state, timestamps) defined in data-model.md
- [x] Validation Rule Consistency: task_validation skill encodes all validation logic
- [x] Input Parsing Centralization: input_parsing skill handles all normalization
- [x] Output Formatting Uniformity: task_formatting skill defines presentation
- [x] Task State Management: task_state_management skill governs transitions
- [x] Error Handling Consistency: error_handling skill standardizes messages

### Skills Policy
- [x] task_validation skill defined
- [x] input_parsing skill defined
- [x] task_formatting skill defined
- [x] error_handling skill defined
- [x] task_state_management skill defined
- [x] Skills encode reusable logic (not UI-specific)
- [x] Skills portable to future phases (CLI → API → Chatbot)
- [x] No duplication across modules planned

**Result**: ✅ Constitution compliance maintained after Phase 1 design.

## Architecture Decisions

### Decision 1: In-Memory List Storage
**Rationale**: Constitution requires in-memory only. Python list provides O(1) random access, O(n) iteration. No external dependencies.

**Trade-offs**:
- Pro: Fast operations, simple implementation, no setup
- Con: Data lost on exit (expected for Phase I)

### Decision 2: Skills as Standalone Modules
**Rationale**: Constitution requires reusable intelligence. Skills as independent modules enable extraction to future phases without modification.

**Trade-offs**:
- Pro: Portable to API, Chatbot, Cloud phases; clear separation of concerns
- Con: Slight overhead in function calls (negligible for CLI scale)

### Decision 3: Menu-Driven CLI
**Rationale**: User stories describe interactive menu flow. Sequential operations (create, view, update, delete) fit menu pattern better than command-line flags.

**Trade-offs**:
- Pro: Intuitive for users, guides through available options
- Con: More keystrokes than command-based CLI for power users (acceptable for Phase I scope)

### Decision 4: String Enumeration for Task Status
**Rationale**: Simple, readable, directly maps to spec requirements. Supports future state extensions without breaking changes.

**Trade-offs**:
- Pro: Self-documenting, easy to debug, extensible
- Con: Slightly more memory than integer codes (negligible)

## Implementation Notes

### Skill Integration Pattern
All business logic functions follow this pattern:
1. Call `input_parsing` skill to normalize input
2. Call `task_validation` skill to validate
3. Perform operation using `task_state_management` skill (if state change)
4. Call `task_formatting` skill to format output
5. Call `error_handling` skill on any errors

### Main Loop Pattern
```python
while True:
    display_main_menu()  # task_formatting skill
    choice = get_user_choice()  # input_parsing skill
    handle_choice(choice)  # business logic orchestrating skills
```

### State Management Pattern
```python
def mark_complete(task_id):
    task = task_list.get_by_id(task_id)  # task_validation checks existence
    if task.status == "completed":
        return error_handling.invalid_state_transition(task_id, "completed")  # task_state_management rejects
    task_state_management.transition(task, "pending", "completed")  # task_state_management validates
    task_list.update(task)
```

## Next Steps

**Phase 2**: `/sp.tasks` - Generate testable implementation tasks from spec and plan

**Artifacts Ready**:
- ✅ Spec: [spec.md](./spec.md) - User stories, requirements, success criteria
- ✅ Research: [research.md](./research.md) - Technical decisions and best practices
- ✅ Data Model: [data-model.md](./data-model.md) - Entities, validation, state transitions
- ✅ Contracts: [contracts/operations.md](./contracts/operations.md) - Operation contracts
- ✅ Quickstart: [quickstart.md](./quickstart.md) - Testing guide
- ✅ Plan: [plan.md](./plan.md) - This file - Architecture and implementation strategy
