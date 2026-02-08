# API Request Handling Skill

## Purpose
Standardize HTTP communication patterns across the frontend application, ensuring consistent API request behavior with proper authentication and state management.

## Behavior Description
This skill provides a unified approach to making API requests that automatically handles authentication headers, request lifecycle states, and error management.

## Core Behaviors
- **Request Standardization**: Apply consistent patterns for all API requests across the application
- **Authentication Attachment**: Automatically include JWT tokens in request headers when available
- **Lifecycle State Management**: Handle loading, success, and error states during API operations
- **Duplicate Prevention**: Prevent redundant API requests and manage concurrent request scenarios

## Scope
- **IN SCOPE**: HTTP request patterns, JWT header attachment, loading/error state management, request deduplication
- **OUT OF SCOPE**: Business logic processing, data transformation, backend operation implementation

## Reusability
This skill can be applied to any component that needs to communicate with backend APIs, ensuring consistent request patterns and authentication handling across all parts of the application.

## Constraints
- Must not implement business logic or data processing
- Cannot modify backend operations or database behaviors
- Limited to frontend request/response handling only
- Cannot validate JWT tokens or authentication claims