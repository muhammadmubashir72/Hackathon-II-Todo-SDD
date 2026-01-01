---
id: 002
title: Create input_parsing skill
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4.5
feature: none
branch: master
user: user
command: create .claude/skills input_parsing skill
labels: [skill, input-parsing, validation, data-normalization]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/input_parsing.md
tests:
  - None
---

## Prompt

Skill Name: input_parsing

Purpose:
User input ko safe, normalized aur error-free banana.

Description:
This skill handles all raw input coming from the CLI interface.
It converts user input into clean, usable data without breaking the application flow.

Responsibilities:

Convert menu selections into valid integers

Trim whitespace from text input

Detect invalid numeric input gracefully

Prevent application crashes due to malformed input

Prompt user again with helpful guidance if input is invalid

Why this is reusable:
CLI, Web forms, aur AI chat commands sab user input dete hain.
Parsing rules ek jaisi rehni chahiye.

## Response snapshot

Created the `input_parsing` skill file at `.claude/skills/input_parsing.md` with comprehensive input parsing and normalization capabilities including:

- Menu selection parsing (integers, range validation)
- Text input normalization (trim, space compression)
- Numeric input validation (integer/float, partial input handling)
- Boolean input parsing (yes/no variations, case-insensitive)
- Graceful error handling with user-friendly messages
- Edge case handling (empty strings, special characters, whitespace)
- Reusability across CLI, Web Forms, and AI Chatbot interfaces
- Anti-patterns to avoid and best practices to follow

## Outcome

- ✅ Impact: Created reusable input parsing skill that safely converts raw user input into clean, validated data across multiple interfaces (CLI, Web Forms, AI Chatbot)
- 🧪 Tests: None
- 📁 Files: Created `.claude/skills/input_parsing.md`
- 🔁 Next prompts: None specific; skill ready for integration
- 🧠 Reflection: Successfully created input_parsing skill following project conventions. The skill handles all major input types (menu selections, text, numeric, boolean) with robust error handling and user-friendly guidance. Reusability is ensured through consistent parsing rules across interfaces.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
