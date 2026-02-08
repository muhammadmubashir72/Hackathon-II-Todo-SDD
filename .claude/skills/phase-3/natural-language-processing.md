# Natural Language Processing Skill

## Purpose
This skill enables the AI assistant to understand and interpret natural language commands for todo management tasks.

## Functions
- Parse user input to identify intent (add, delete, update, list, complete)
- Extract relevant entities (task titles, dates, priorities, categories)
- Validate user commands for completeness and correctness
- Generate appropriate responses based on processing results

## Input Format
- Raw user input string in natural language
- Contextual information (current conversation state, user preferences)

## Output Format
- Structured command object with intent and parameters
- Validation status and error messages if applicable
- Confidence score for interpretation accuracy

## Examples
Input: "Add a task to buy groceries tomorrow"
Output: {intent: "add_task", parameters: {title: "buy groceries", date: "tomorrow"}}

Input: "Show me all urgent tasks"
Output: {intent: "list_tasks", parameters: {filter: "urgent"}}

Input: "Mark the meeting task as complete"
Output: {intent: "complete_task", parameters: {reference: "meeting"}}

## Error Handling
- Provide helpful suggestions when input is ambiguous
- Ask for clarification when multiple interpretations exist
- Gracefully handle unrecognized commands