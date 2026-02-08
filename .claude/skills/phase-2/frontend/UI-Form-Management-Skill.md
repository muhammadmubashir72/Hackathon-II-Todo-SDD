# UI Form Management Skill

## Purpose
Handle form state, validation, and user interactions consistently across all forms in the frontend application.

## Behavior Description
This skill provides standardized form handling behavior that manages user input, validation, and submission states while providing appropriate user feedback.

## Core Behaviors
- **Form State Management**: Track and manage form field values and their changes over time
- **Validation Handling**: Apply consistent validation rules and handle empty or invalid inputs gracefully
- **Submission Control**: Disable form submissions during active API calls to prevent duplicate submissions
- **Feedback Presentation**: Show clear, user-friendly validation feedback and error messages

## Scope
- **IN SCOPE**: Form state tracking, input validation, submission state management, user feedback presentation
- **OUT OF SCOPE**: Business rule validation, backend data validation, database operations, form layout or styling

## Reusability
This skill can be applied to any form component in the application, ensuring consistent form behavior regardless of the specific form type or purpose (login, signup, task creation, etc.).

## Constraints
- Must not implement business rule validation or complex validation logic
- Cannot access backend validation or database operations
- Limited to frontend form state and user experience management
- Cannot modify data processing or storage mechanisms