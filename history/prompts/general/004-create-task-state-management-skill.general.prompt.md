---
id: 004
title: Create task_state_management skill
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4.5
feature: none
branch: master
user: user
command: create .claude/skills task_state_management skill
labels: [skill, state-management, task-lifecycle, data-integrity]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/task_state_management.md
tests:
  - None
---

## Prompt

Skill Name: task_state_management

Purpose:
Task lifecycle ko control aur maintain karna.

Description:
This skill governs how tasks move between states (active, completed).

Responsibilities:

Toggle task completion status safely

Ensure task state remains valid

Prevent invalid state transitions

Keep task state logic centralized

Why this is reusable:
Task lifecycle rules future features (due dates, reminders, priorities) ke foundation bante hain.

## Response snapshot

Created the `task_state_management` skill file at `.claude/skills/task_state_management.md` with comprehensive state management capabilities including:

- Task states (Pending, Completed, future states: In Progress, Blocked, Archived)
- Valid state transitions (Pending ↔ Completed)
- State transition rules (existence check, valid transition, duplicate prevention, history tracking)
- Core state operations (complete, incomplete/reopen, toggle)
- Batch state operations (complete multiple, complete all pending)
- State queries (check state, count by state, get tasks by state)
- State validation workflow with examples
- Error handling for invalid transitions
- State persistence with data model and invariants
- Reusability for future features (due dates, reminders, priorities, dependencies)
- Best practices and anti-patterns

## Outcome

- ✅ Impact: Created task state management skill that provides safe, centralized control over task lifecycle with valid transitions, history tracking, and error handling. Foundation for future features like due dates, reminders, and task dependencies.
- 🧪 Tests: None
- 📁 Files: Created `.claude/skills/task_state_management.md`
- 🔁 Next prompts: None specific; skill ready for integration
- 🧠 Reflection: Successfully created task_state_management skill following project conventions. The skill handles core state transitions (pending ↔ completed) with comprehensive validation, history tracking, and batch operations. Centralized state logic ensures consistency and provides foundation for future features like due dates, reminders, and task dependencies.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
