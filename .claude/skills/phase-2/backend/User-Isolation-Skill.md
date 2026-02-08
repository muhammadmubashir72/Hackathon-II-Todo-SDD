# User-Isolation Skill

## Purpose
Enforces user-level data access controls across the backend system. Ensures all database queries and API operations are properly scoped to the current authenticated user. Prevents cross-user data leakage and unauthorized access to other users' information. Maintains data privacy and security through consistent isolation mechanisms.

## Capabilities
- Inject user ID into database queries automatically
- Verify resource ownership before operations
- Prevent unauthorized cross-user access
- Enforce data isolation at database layer
- Validate user permissions for shared resources

## Responsibilities
- Ensure all database queries are scoped to authenticated user
- Verify user ownership before update/delete operations
- Prevent access to other users' data
- Inject user filters into query builders
- Validate user permissions for shared resources
- Handle multi-tenant data separation
- Log access violations for security monitoring
- Enforce isolation at both API and database layers

## Constraints
- Backend-only implementation (no frontend concerns)
- Apply to all user-specific data operations
- Ensure no cross-user data leakage occurs
- Maintain performance while enforcing isolation
- Work with FastAPI security dependencies
- Integrate with SQLModel query mechanisms
- Support concurrent user access safely
- Follow database security best practices