---
id: 001
title: Create task_validation skill
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4.5
feature: none
branch: master
user: user
command: create .claude/skills task_validation skill
labels: [skill, validation, task-management, data-integrity]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/task_validation.md
tests:
  - None
---

## Prompt

create .claude/skills Skill Name: task_validation

Purpose:
Ensure ke Todo app me har task operation safe, consistent aur predictable ho.

Description:
This skill is responsible for validating all task-related actions.
It ensures that task data follows the agreed rules before any operation is executed.

Responsibilities:

Ensure task title is not empty

Ensure task ID exists before update, delete, or complete actions

Prevent duplicate or invalid task references

Return clear, human-readable error messages instead of raw exceptions

Why this is reusable:
Same validation rules Phase I (CLI), Phase II (API), aur Phase III (AI Chatbot) me unchanged reuse hongi.

## Response snapshot

Created the `task_validation` skill file at `.claude/skills/task_validation.md` with comprehensive validation rules including:

- Task title validation (non-empty, min/max length)
- Task ID validation (existence check, format validation)
- Duplicate prevention
- Human-readable error handling in Hinglish
- Reusability across Phase I, II, and III
- Detailed edge case handling
- Structured output format for success/failure cases

## Outcome

- ✅ Impact: Created reusable validation skill for Todo app task operations that can be used across CLI, API, and AI Chatbot phases
- 🧪 Tests: None
- 📁 Files: Created `.claude/skills/task_validation.md`
- 🔁 Next prompts: None specific; skill ready for integration
- 🧠 Reflection: Successfully created task_validation skill following project conventions. The skill provides comprehensive validation rules with clear error messages in Hinglish. Reusability across all three phases (CLI, API, AI Chatbot) is ensured by maintaining consistent validation logic.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
