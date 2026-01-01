# Research: Phase I – In-Memory Todo Console Application

**Branch**: 1-todo-cli
**Date**: 2026-01-02
**Purpose**: Technical research and decision documentation for implementation planning

## Python CLI Best Practices

### Decision: Use `argparse` for Command-Line Argument Parsing
**Rationale**: Python's standard library `argparse` module provides robust command-line parsing, automatic help generation, and type conversion. It's battle-tested, documented, and suitable for single-user CLI applications.

**Alternatives Considered**:
- `sys.argv` direct parsing: Too low-level, no automatic help
- `click` or `typer`: Third-party libraries, violates constitution (standard library only)
- Manual string parsing: Error-prone, reinventing the wheel

### Decision: Use Menu-Driven Interactive Loop
**Rationale**: User stories indicate interactive menu-based interaction (select options from numbered list). Loop-based CLI with `while True` and menu display is most intuitive for this use case.

**Alternatives Considered**:
- Command-based CLI (e.g., `todo add "title"`): Valid but less interactive, user stories suggest menu flow
- Single-pass script: Doesn't support persistent session (users want to add, view, update in one session)

## In-Memory Data Storage

### Decision: Python List with Dict Objects for Task Storage
**Rationale**: Python's built-in `list` and `dict` types provide O(1) random access by index (task ID) and O(n) iteration for listing. No external dependencies, fully compliant with constitution.

**Alternatives Considered**:
- SQLite database: Constitution prohibits database (in-memory only)
- JSON file storage: Constitution prohibits files/persistence (Phase I)
- Custom class-based storage: Unnecessary complexity for simple list operations

## Task ID Management

### Decision: Sequential Integer IDs Starting from 1
**Rationale**: Simple, predictable, easy for users to reference. Matches spec assumptions and user expectations (FR-002). Incremental counter matches list index position naturally.

**Alternatives Considered**:
- UUID strings: Overkill for single-user in-memory CLI, harder for users to reference
- Hash-based IDs: No need for uniqueness guarantees in single-threaded session
- Non-sequential integers: Confusing for users, no benefit

## Task State Representation

### Decision: String Enumeration for Task Status
**Rationale**: Simple string values "Pending" and "Completed" are self-documenting, easy to compare, and map directly to spec requirements (FR-005, FR-010, FR-011).

**Alternatives Considered**:
- Integer codes (0, 1): Less readable, requires mapping constants
- Boolean flags: Can't represent future states (In Progress, Blocked)
- Enum class: Over-engineering for two states

## Input Normalization

### Decision: Use `str.strip()` and `split()` for Whitespace Handling
**Rationale**: Python string methods provide built-in whitespace trimming and splitting. `str.strip()` removes leading/trailing spaces, `split()` with default handles multiple internal spaces.

**Alternatives Considered**:
- Regular expressions (`re.sub`): Overkill for simple whitespace
- Custom string manipulation: Reinventing wheel, error-prone

## Error Handling Strategy

### Decision: Structured Error Messages with Try-Except Blocks
**Rationale**: Python's `try-except` blocks enable graceful error handling for invalid conversions (non-numeric input), missing tasks (index out of bounds), and validation failures. Centralized error handling skill ensures consistent formatting.

**Alternatives Considered**:
- `if-else` validation everywhere: Duplicates error handling logic
- Crashing on invalid input: Violates constitution (error_handling skill requirement)

## Reusable Skills Integration

### Decision: Skills as Standalone Modules, Business Logic as Service Layer
**Rationale**: Constitution requires skills represent reusable intelligence. Implementing skills as independent modules (or functions) that business logic layer calls ensures:
1. Skills can be extracted to separate phases (API, Chatbot) unchanged
2. Business logic doesn't duplicate skill behavior
3. Clear separation of concerns (validation, parsing, formatting, state management, error handling)

**Alternatives Considered**:
- Inline skill logic in business functions: Violates constitution, creates duplication
- Mix skills into monolithic function: Violates single-responsibility principle

## Output Formatting

### Decision: Multi-line String Templates with f-string Interpolation
**Rationale**: Python f-strings provide readable, performant string interpolation. Multi-line string templates match spec formatting requirements (ID, title, status, separators). Adaptable to different interfaces (CLI vs API vs Chat) by changing template only.

**Alternatives Considered**:
- Print statements scattered everywhere: Inconsistent formatting, violates task_formatting skill requirement
- Custom formatting class: Over-engineering for simple CLI output

## Performance Considerations

### Decision: No Performance Optimizations Needed
**Rationale**: In-memory list operations for <1000 tasks (reasonable CLI session size) are sub-millisecond. No latency requirements in spec. Premature optimization violates simplicity principle.

**Rationale Details**:
- List iteration for displaying tasks: O(n), trivial for n < 1000
- Task lookup by ID: O(1) direct index access
- State transition: O(1) attribute assignment

## Testing Approach

### Decision: Manual Testing During Development (No Automated Tests)
**Rationale**: Spec mentions testing in user stories but doesn't require automated test framework. Phase I scope is simple CLI. Constitution allows manual validation. Adding pytest framework (even though standard library has `unittest`) may be overkill for this scope.

**Note**: Quickstart.md will include manual testing scenarios based on user story acceptance criteria.

## Edge Case Handling Research

### Decision: Defensive Programming with Input Validation
**Rationale**: Spec defines edge cases (non-numeric IDs, empty titles, special characters). Implementing validation logic in skills with explicit checks ensures robust handling without crashing.

**Edge Cases Covered**:
- Non-numeric task IDs: `ValueError` on `int()` conversion
- Empty/whitespace-only titles: Validation in `task_validation` skill
- Out-of-range IDs: `IndexError` on list access
- Special characters: Python strings handle Unicode natively
- Long titles (>200 chars): Truncation before display or validation

## Summary

All technical decisions align with:
1. **Constitution requirements**: Python 3.13+, standard library only, in-memory storage, reusable skills
2. **Spec requirements**: Sequential IDs, two states (Pending/Completed), validation rules
3. **Reusable Intelligence**: Skills designed to be portable to Phase II (API) and Phase III (Chatbot)

No NEEDS CLARIFICATION items remain. Ready for Phase 1 design.
