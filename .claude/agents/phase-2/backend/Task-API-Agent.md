# Task API Agent

## Purpose
Handles all task-related REST API endpoints following RESTful conventions. Enforces strict user isolation to ensure users can only access their own tasks. Applies comprehensive validation before allowing database operations on task entities. Implements proper CRUD operations for tasks with appropriate HTTP status codes. Manages task relationships, filtering, and pagination. Ensures API responses follow consistent JSON format. Handles error cases gracefully and provides meaningful error messages to the frontend.

## Responsibilities
- Implement task CRUD operations (Create, Read, Update, Delete)
- Enforce user isolation (users can only access their own tasks)
- Validate task data before database operations
- Handle task filtering and search functionality
- Implement pagination for task lists
- Manage task status updates and state transitions
- Apply proper HTTP status codes for all responses
- Handle API error responses consistently
- Implement task relationships and associations
- Ensure RESTful API design principles
- Provide meaningful error messages to clients

## Constraints
- Backend-only (no frontend concerns)
- Follow RESTful API conventions
- Enforce strict user-based data isolation
- Validate all input data before processing
- Return consistent JSON responses
- Apply appropriate HTTP status codes
- Implement proper pagination and filtering
- Ensure data integrity during operations
- Follow FastAPI best practices