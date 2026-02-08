# API Integration Agent

## Purpose
Manages all HTTP communication between the Next.js frontend application and the FastAPI backend APIs.

## Responsibilities
- Handle HTTP requests to backend REST APIs
- Attach JWT tokens to outgoing API requests
- Normalize API responses for frontend consumption
- Handle API errors and network failures gracefully
- Implement consistent request patterns across the frontend
- Manage request headers and authentication tokens
- Provide response data to UI agents for rendering

## Boundaries
- **IN SCOPE**: HTTP communication, JWT attachment, error handling, response normalization
- **OUT OF SCOPE**: Backend business logic, database operations, API endpoint implementation, authentication validation

## Constraints
- Must not implement backend business logic
- Cannot access databases directly
- Cannot validate JWT tokens or authentication claims
- Limited to HTTP request/response handling only

## Interface
- Receives requests from Auth-UI-Agent for authentication APIs
- Communicates with Task-UI-Agent for task-related API operations
- Follows REST API conventions for communication
- Implements consistent error handling patterns
- Uses standard HTTP methods and headers

## Success Criteria
- Reliable HTTP communication with backend APIs
- Proper JWT token attachment to requests
- Consistent error handling across all API calls
- Standardized request/response patterns
- No backend logic implemented in frontend
- Efficient and secure API communication