# Authentication Skill

## Purpose
Provides secure authentication functionality for the backend system. Handles password hashing and verification using industry-standard algorithms. Generates and validates JWT tokens for session management. Safely extracts user identity from authenticated requests. Ensures all authentication processes follow security best practices.

## Capabilities
- Hash passwords using bcrypt or similar secure algorithm
- Verify password hashes during login process
- Generate JWT tokens with appropriate claims and expiration
- Validate JWT tokens and extract user identity
- Refresh expired tokens when applicable
- Handle authentication errors securely

## Responsibilities
- Securely hash passwords before storing in database
- Verify submitted passwords against stored hashes
- Generate JWT tokens with user identity claims
- Validate incoming JWT tokens in protected endpoints
- Extract user ID or identity from validated tokens
- Handle token expiration and refresh scenarios
- Log authentication attempts for security monitoring
- Prevent timing attacks during password verification

## Constraints
- Backend-only implementation (no frontend concerns)
- Use industry-standard security practices (bcrypt, JWT)
- Never expose sensitive credentials in logs
- Implement proper rate limiting for authentication endpoints
- Follow JWT best practices for token security
- Ensure tokens have appropriate expiration times
- Protect against token hijacking and replay attacks
- Maintain user privacy during authentication process