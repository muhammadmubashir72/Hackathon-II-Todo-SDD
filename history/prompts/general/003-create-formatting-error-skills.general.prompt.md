---
id: 003
title: Create task_formatting and error_handling skills
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4.5
feature: none
branch: master
user: user
command: create .claude/skills task_formatting and error_handling skills
labels: [skill, task-formatting, error-handling, user-experience]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/task_formatting.md
  - .claude/skills/error_handling.md
tests:
  - None
---

## Prompt

Skill Name: task_formatting

Purpose:
Tasks ko consistently aur clearly display karna.

Description:
This skill defines how task data is presented to the user.
It ensures a uniform, readable output format across the application.

Responsibilities:

Display task ID, title, and completion status clearly

Show completed vs incomplete tasks distinctly

Format task lists in a clean, readable layout

Keep output style consistent across all views

Why this is reusable:
Same formatting logic CLI output, API responses, aur Chat UI me adapt ho sakti hai.

4️⃣ Error Handling Skill

Skill Name: error_handling

Purpose:
Errors ko user-friendly aur controlled way me handle karna.

Description:
This skill standardizes how errors are generated and displayed.
It avoids technical jargon and focuses on clarity.

Responsibilities:

Catch logical errors before runtime failures

Display meaningful error messages

Avoid stack traces or raw exceptions in user-facing output

Keep error tone polite and helpful

Why this is reusable:
Error experience Phase I se Phase V tak consistent rehna chahiye.

## Response snapshot

Created two comprehensive skill files:

1. **task_formatting.md** - Task display and presentation skill:
   - Single task format (ID, title, status, dates)
   - Task list format with clean layout
   - Completion status indicators (✓/✅ vs [ ]/⬜)
   - Visual design principles (readability, contrast, consistency)
   - Multiple output variants (CLI, API JSON, Chat UI)
   - Special cases (empty lists, long titles, tags, priority)
   - Text truncation, date/time formatting rules
   - Reusable across CLI, API, and Chat interfaces

2. **error_handling.md** - User-friendly error management skill:
   - Error classification (validation, business logic, system, network)
   - Structured error message format
   - Good vs bad error message examples
   - Error recovery strategies (suggest input, provide examples, offer retry, alternatives)
   - Severity levels (informational ℹ️, warning ⚠️, error ❌, critical 🚨)
   - Special error scenarios (empty list, duplicate, permission denied, concurrent modification)
   - Error tone guidelines (polite, supportive, clear, empathetic)
   - Reusable across Phase I to Phase V for consistent error experience

## Outcome

- ✅ Impact: Created two critical user experience skills - task_formatting for consistent task display and error_handling for user-friendly error management across all phases
- 🧪 Tests: None
- 📁 Files: Created `.claude/skills/task_formatting.md` and `.claude/skills/error_handling.md`
- 🔁 Next prompts: None specific; both skills ready for integration
- 🧠 Reflection: Successfully created task_formatting and error_handling skills following project conventions. Task formatting ensures consistent, readable display across CLI, API, and Chat UI. Error handling provides structured, user-friendly error messages with recovery strategies and appropriate severity levels. Together these skills ensure a consistent, professional user experience across all phases.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
