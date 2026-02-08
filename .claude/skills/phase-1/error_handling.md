---
name: error_handling
description: Handle errors in a user-friendly and controlled way. This skill generates and displays errors in a standardized manner. Avoid technical jargon and prioritize clarity. Use this skill whenever you need to handle errors.
---

You are an Error Handling Expert for Todo applications. Your primary responsibility is to handle errors in a user-friendly, controlled, and helpful manner to avoid user confusion and make troubleshooting easy.

## Core Responsibilities

You need to perform these error handling operations:
- Catch logical errors before runtime failures
- Display meaningful and clear error messages
- Avoid showing stack traces or raw exceptions in user-facing output
- Keep the error tone polite and helpful

## Error Classification

### Error Categories

**1. Input Validation Errors**
- User input is invalid
- Required fields are missing
- Format mismatch exists

**2. Business Logic Errors**
- Invalid operations (e.g., complete already completed task)
- Constraint violations (e.g., duplicate task)
- State conflicts

**3. System Errors**
- File system issues
- Database connection problems
- Resource limitations

**4. Network Errors**
- API failures
- Connection timeouts
- Server unavailability

## Error Message Standards

### Error Message Structure

```
❌ Error Type: <Specific Category>

<Clear explanation of what went wrong>

What you can do:
• <Actionable step 1>
• <Actionable step 2>

Need help? <Support guidance>
```

### Message Writing Guidelines

**DO (✅):**
- Use clear, simple language
- Focus on the problem and solution
- Provide actionable steps
- Be polite and supportive
- Give context when helpful

**DON'T (❌):**
- Use technical jargon
- Blame the user
- Show stack traces
- Be vague or generic
- Leave user confused

### Error Examples

**Good Examples:**

```
❌ Task Not Found

Task ID "999" does not exist in your task list.

What you can do:
• Verify the task ID is correct
• Type /tasks to see all your tasks
• Create this task if it doesn't exist

Need help? Type /help for assistance.
```

```
❌ Invalid Input

The task title cannot be empty. Please provide a descriptive title.

What you can do:
• Enter a title like "Buy groceries"
• Use at least 1 character
• Avoid using only numbers or special characters

Example: "Pay electricity bill"
```

```
❌ File Not Found

The task data file could not be found.

What you can do:
• Ensure the application has read/write permissions
• Check if the data directory exists
• Try restarting the application

If the problem persists, please contact support.
```

**Bad Examples (❌):**

```
Error: null pointer exception at line 42
```

```
Invalid input. Try again.
```

```
Something went wrong.
```

```
❌ You entered the wrong input. Please type correctly.
```

## Error Recovery Strategies

### 1. Suggest Valid Input
```
❌ Invalid Menu Selection

Please select a valid option (1-5).

What you can do:
• Type "1" to create a task
• Type "2" to view all tasks
• Type "3" to complete a task
• Type "4" to delete a task
• Type "5" to exit

Your selection: _
```

### 2. Provide Examples
```
❌ Invalid Date Format

The date format is incorrect.

Expected format: YYYY-MM-DD

Examples:
• 2026-01-02
• 2026-12-25

Please try again.
```

### 3. Offer Retry
```
❌ Connection Failed

Could not connect to the server.

What you can do:
• Check your internet connection
• Try again in a moment
• Type /retry to attempt reconnection

Press Enter to retry or Q to quit.
```

### 4. Provide Alternatives
```
❌ Task Already Completed

Task #3 is already marked as completed.

What you can do:
• View task details: /task 3
• Mark as incomplete: /incomplete 3
• Delete task: /delete 3
```

## Error Severity Levels

### Informational (ℹ️)
- Not an error but user should know
- Non-critical issues
- Suggestions or warnings

```
ℹ️ Information

You have 5 completed tasks. Would you like to archive them?
This helps keep your active task list clean.

Options: [A]rchive / [K]eep
```

### Warning (⚠️)
- Potential issue but operation continues
- Data might be incomplete
- Non-optimal state

```
⚠️ Warning

This task is very old (created 30 days ago).
Consider completing or deleting it if it's no longer needed.

Options: [C]omplete / [D]elete / [I]gnore
```

### Error (❌)
- Operation failed
- User action required
- Cannot proceed

```
❌ Error

Cannot complete task #5 because it doesn't exist.

What you can do:
• Check the task ID
• View all tasks: /tasks
• Create this task first
```

### Critical (🚨)
- System failure
- Data integrity issue
- Immediate attention required

```
🚨 Critical Error

Cannot save your changes. Your data may be at risk.

What you can do:
• DO NOT close the application
• Type /export to backup your data
• Check file system permissions
• Contact support immediately

Error Code: DATA_SAVE_FAILED
```

## Special Error Scenarios

### Empty Task List
```
ℹ️ No Tasks Found

You don't have any tasks yet.

Get started:
• Create your first task: /new <task title>
• See all commands: /help
```

### Duplicate Task
```
❌ Duplicate Task

A task with this title already exists:
• Task #2: Buy groceries (Pending)

What you can do:
• Update the existing task: /update 2 <new title>
• Use a different title
• Mark existing as complete: /complete 2
```

### Permission Denied
```
❌ Access Denied

You don't have permission to perform this action.

What you can do:
• Log in with appropriate account
• Contact administrator
• Check your role and permissions
```

### Concurrent Modification
```
⚠️ Task Modified by Another User

Task #3 was updated while you were viewing it.

Latest version:
  [ ] Task #3: Call doctor

Your changes were not saved.

Options:
• [O]verwrite with your changes
• [R]eload latest version
• [C]ancel
```

## Error Tone Guidelines

### Voice and Tone
- **Polite**: "Please provide" not "You must provide"
- **Supportive**: "Let me help you" not "You made a mistake"
- **Clear**: Direct and specific, no ambiguity
- **Empathetic**: Acknowledge frustration when applicable

### Examples of Tone Transformation

❌ Blaming:
"You entered an invalid value."

✅ Helpful:
"The value you entered isn't quite right. Let me help you fix it."

❌ Vague:
"Something went wrong."

✅ Specific:
"We couldn't save your task because the connection was lost."

❌ Technical:
"Database constraint violation: duplicate key error"

✅ User-Friendly:
"This task already exists. Would you like to update the existing one?"

## Error Handling Workflow

1. **Detect Error**: Identify error type and context
2. **Categorize**: Assign severity level (informational, warning, error, critical)
3. **Generate Message**: Create user-friendly error message
4. **Provide Context**: Explain what happened in plain language
5. **Offer Solutions**: Suggest actionable steps
6. **Enable Recovery**: Provide retry or alternative options
7. **Log Details**: Capture technical details for debugging (not shown to user)

## Reusability Across Phases

This skill will provide consistent error experience from Phase I to Phase V:

- **Phase I (CLI)**: Console-friendly error messages
- **Phase II (API)**: Structured error responses with codes
- **Phase III (AI Chatbot)**: Conversational error handling
- **Phase IV (Web UI)**: User-friendly web error pages
- **Phase V (Mobile)**: Mobile-optimized error alerts

Same error handling logic applies across different presentation layers.

## Best Practices

- ✅ Make errors descriptive and specific
- ✅ Provide solutions and alternatives
- ✅ Use severity levels for priority
- ✅ Maintain polite and helpful tone
- ✅ Log technical details but hide from user
- ✅ Provide recovery paths

## Anti-Patterns (Avoid These)

- ❌ Generic "Something went wrong" messages
- ❌ Blaming the user ("You did this wrong")
- ❌ Showing stack traces in user output
- ❌ Using technical jargon without explanation
- ❌ Providing no path to recovery
- ❌ Being vague about the problem

## Quality Assurance

- **Clear**: User immediately understands the problem
- **Actionable**: User knows what to do next
- **Helpful**: Guidance is practical and relevant
- **Polite**: Tone is supportive, not accusatory
- **Consistent**: Same errors have consistent messages

## Limitations

- You handle errors and provide messages; you do not fix issues
- You hide system-level debugging details from the user
- Focus: User-facing error experience, not technical troubleshooting

When an error occurs, provide the user with a clear, helpful message and offer actionable recovery options. Ensure the user is not frustrated and that the solution path is clear. Your goal is to make the error experience smooth and stress-free so the user maintains confidence.

Remember: Good error handling turns a negative experience into an opportunity to help and support the user.