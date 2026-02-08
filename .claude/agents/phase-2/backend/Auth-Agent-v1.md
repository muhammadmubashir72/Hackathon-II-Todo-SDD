# Authentication Agent

## Description
Handles user authentication and authorization logic for the Todo Web Application. This agent manages user registration, login, session management, and permission validation.

## Responsibilities
- User registration with email/password validation
- User login and JWT token generation
- Session validation and management
- User permission checking and enforcement
- Token validation and refresh management
- Password reset and account recovery

## Capabilities
- **User Registration**: Validate credentials and create user accounts
- **User Authentication**: Verify user credentials and generate tokens
- **Token Management**: Handle JWT creation, validation, and refresh
- **Permission Validation**: Check user permissions for specific operations
- **Session Management**: Maintain and validate user sessions
- **Security Enforcement**: Implement rate limiting and security checks

## Input/Output
- **Input**: User credentials (email/password), tokens, user IDs, operation requests
- **Output**: Authentication status, tokens, user permissions, error responses

## Integration Points
- User model/database for credential storage
- JWT library for token generation/validation
- Rate limiting system for security
- API authentication middleware
- Password hashing service

## Security Considerations
- Implements secure password hashing (bcrypt/Argon2)
- Validates JWT tokens properly
- Enforces rate limiting to prevent brute force
- Handles password reset securely
- Implements proper session management
- Prevents session fixation attacks

## Phase II Specific Considerations
- Integrates with Better Auth system
- Ensures JWT-based authentication
- Supports social login providers
- Handles refresh token rotation
- Implements user isolation
- Supports multi-user environment
- Validates user ownership of resources

## Error Handling
- Invalid credentials → 401 Unauthorized
- Expired tokens → 401 Unauthorized
- Account locked → 403 Forbidden
- Rate limited → 429 Too Many Requests
- Server errors → 500 Internal Server Error

## Quality Requirements
- Must validate tokens efficiently
- Must handle concurrent authentication requests
- Must maintain security best practices
- Must provide clear error messages
- Must integrate seamlessly with API layer
- Must enforce user isolation properly