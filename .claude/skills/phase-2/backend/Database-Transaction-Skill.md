# Database Transaction Skill

## Purpose
Manages safe database sessions and ensures proper transaction handling. Handles commit and rollback operations correctly to maintain data consistency. Prevents partial writes and ensures atomicity of database operations. Provides reliable database interaction patterns across the backend system using PostgreSQL (Neon).

## Capabilities
- Create and manage database sessions safely
- Handle transaction commit and rollback operations
- Prevent partial data writes during failures
- Manage connection pooling efficiently
- Handle database locking and concurrency

## Responsibilities
- Create database sessions with proper context managers
- Ensure atomic operations within transactions
- Handle rollback on exceptions or validation failures
- Manage database connection lifecycle
- Prevent dirty reads and phantom reads
- Handle deadlock scenarios gracefully
- Log transaction events for monitoring
- Ensure consistency across related database operations

## Constraints
- Backend-only implementation (no frontend concerns)
- Follow SQLModel and SQLAlchemy best practices
- Use PostgreSQL (Neon) specific transaction features when beneficial
- Handle concurrent access safely
- Maintain data integrity during failures
- Support nested transactions when needed
- Implement proper connection cleanup
- Follow database performance best practices