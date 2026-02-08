# API Error Handling Skill

## Purpose
Normalizes API errors and ensures consistent HTTP responses across the backend system. Hides internal exceptions from clients while providing meaningful error information to API consumers. Provides standardized error response formats that follow REST API best practices.

## Capabilities
- Normalize different error types to consistent responses
- Map internal exceptions to appropriate HTTP status codes
- Generate user-friendly error messages
- Log internal errors for debugging while protecting clients
- Provide structured error responses with codes and details

## Responsibilities
- Convert internal exceptions to appropriate HTTP status codes
- Generate consistent error response formats
- Hide sensitive internal information from client responses
- Provide meaningful error messages for API consumers
- Log errors for debugging and monitoring purposes
- Maintain error response schema consistency
- Handle validation errors appropriately
- Support internationalization of error messages when needed

## Constraints
- Backend-only implementation (no frontend concerns)
- Follow REST API error response conventions
- Never expose internal system details to clients
- Use appropriate HTTP status codes (4xx, 5xx)
- Maintain consistent error response structure
- Support structured logging for errors
- Follow security best practices for error disclosure
- Ensure performance during error handling