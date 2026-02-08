# Task Rendering Skill

## Purpose
Provide consistent rendering and state management for task-related UI elements across the frontend application.

## Behavior Description
This skill ensures uniform presentation of task data and maintains synchronization between UI state and backend API responses for all task-related operations.

## Core Behaviors
- **Consistent Rendering**: Display task lists with standardized formatting and visual representation
- **Status Reflection**: Clearly indicate task completion status and other relevant states in the UI
- **Response Integration**: Update UI elements based on API response data to reflect backend changes
- **State Synchronization**: Keep frontend UI state synchronized with backend data changes

## Scope
- **IN SCOPE**: Task list presentation, status visualization, UI updates based on API responses, state synchronization
- **OUT OF SCOPE**: Task business logic, backend data processing, database operations, task algorithm implementation

## Reusability
This skill can be applied to any component that displays or interacts with task data, ensuring consistent task presentation and behavior across different views and pages.

## Constraints
- Must not implement task business logic or processing algorithms
- Cannot access or modify backend operations or database systems
- Limited to frontend presentation and state management only
- Cannot alter task data processing or storage mechanisms