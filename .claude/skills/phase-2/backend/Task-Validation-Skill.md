# Task Validation Skill

## Purpose
Validates task input data and ensures proper task ownership before database operations. Provides comprehensive validation for task-related data structures. Ensures that update and delete operations are only performed on tasks owned by the authenticated user. Returns clear, consistent error messages for API responses.

## Capabilities
- Validate task input data against schema requirements
- Check task ownership before modification operations
- Sanitize task data before database insertion
- Validate task relationships and dependencies
- Return standardized error responses for validation failures

## Responsibilities
- Validate required task fields (title, description, etc.)
- Check character limits and data type constraints
- Ensure task ownership before update/delete operations
- Validate task status transitions
- Sanitize user input to prevent injection attacks
- Verify task relationships and dependencies
- Return clear error messages for validation failures
- Support bulk task validation when applicable
- Handle edge cases in task validation

## Constraints
- Backend-only implementation (no frontend logic)
- Follow FastAPI validation patterns
- Integrate with Pydantic models for validation
- Return consistent error response formats
- Support both individual and bulk task validation
- Maintain performance during validation
- Follow REST API error response conventions
- Prevent validation bypass attempts