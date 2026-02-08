# Error Display Skill

## Purpose
Provide consistent, user-friendly error messaging across the frontend application while hiding technical implementation details.

## Behavior Description
This skill standardizes error presentation to ensure users receive clear, actionable feedback without exposing sensitive technical information from API responses.

## Core Behaviors
- **Unified Error Presentation**: Display errors with consistent styling and positioning across all application pages
- **Technical Information Hiding**: Transform raw API error messages into user-friendly content that avoids exposing system internals
- **Behavioral Consistency**: Apply uniform error handling behavior regardless of the error source or page location
- **User Guidance**: Provide appropriate guidance or next steps when errors occur

## Scope
- **IN SCOPE**: Error message formatting, user-friendly presentation, consistent display behavior, error state management
- **OUT OF SCOPE**: Error logging, backend error resolution, exception handling at the system level, debugging information

## Reusability
This skill can be applied to any component that needs to display errors to users, ensuring a consistent error experience across authentication, task operations, API communications, and other application features.

## Constraints
- Must not log errors to backend systems or perform server-side error handling
- Cannot expose technical details, stack traces, or system information to users
- Limited to frontend error presentation and user experience management
- Cannot modify error handling at the API or backend level