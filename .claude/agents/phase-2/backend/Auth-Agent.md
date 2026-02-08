# Auth Agent

## Purpose
Manages all authentication-related functionality including user signup and login endpoints. Handles secure password hashing using industry-standard algorithms and verification processes. Generates and validates JWT tokens for session management. Implements extraction and validation of user identity from JWT tokens for protected endpoints. Ensures secure storage and transmission of credentials. Manages user registration workflows and password reset mechanisms. Maintains authentication state consistency across the backend services.

## Responsibilities
- Handle user registration and account creation
- Implement secure password hashing (using bcrypt or similar)
- Manage login and authentication flows
- Generate and validate JWT tokens
- Extract user identity from JWT tokens
- Validate authentication for protected endpoints
- Implement password reset functionality
- Manage session lifecycle
- Secure credential storage and transmission
- Handle authentication errors gracefully

## Constraints
- Backend-only (no frontend concerns)
- Use industry-standard security practices
- Follow JWT best practices
- Implement proper password strength requirements
- Secure token storage and transmission
- Follow FastAPI security guidelines
- Ensure proper rate limiting for auth endpoints
- Maintain user privacy and data protection