# Database Agent

## Description
Handles all database interactions for the Todo Web Application. This agent manages connections, queries, transactions, and data operations using SQLModel with Neon Serverless PostgreSQL.

## Responsibilities
- Execute database queries for all entities (users and tasks)
- Manage database transactions for data consistency
- Handle connection pooling for efficiency
- Perform CRUD operations on users and tasks
- Manage user and task data operations
- Handle database migrations and schema management

## Capabilities
- **Query Execution**: Execute SELECT, INSERT, UPDATE, DELETE operations
- **Transaction Management**: Handle ACID properties for complex operations
- **Connection Management**: Manage connection pooling and lifecycle
- **CRUD Operations**: Perform create, read, update, delete operations
- **Data Validation**: Validate data before database operations
- **Error Handling**: Handle database-specific errors and constraints

## Input/Output
- **Input**: Database operation requests, query parameters, entity data, user context
- **Output**: Query results, operation confirmations, error responses, transaction status

## Integration Points
- SQLModel for ORM operations
- Neon Serverless PostgreSQL for database
- User models for user operations
- Task models for task operations
- API controllers for data requests
- Authentication system for user validation

## Database Operations
- **User Operations**: Create, read, update, delete user records
- **Task Operations**: Create, read, update, delete task records
- **Query Operations**: Filter, sort, and paginate data
- **Relationship Operations**: Handle user-task relationships
- **Transaction Operations**: Complex multi-table operations
- **Index Operations**: Optimize queries with proper indexing

## Security Considerations
- Uses parameterized queries to prevent SQL injection
- Implements proper access controls for data operations
- Validates user permissions before database operations
- Handles sensitive data securely
- Implements proper error handling without information disclosure
- Manages connection security with SSL if applicable

## Performance Considerations
- Implements connection pooling for efficiency
- Uses proper indexing for query optimization
- Handles large dataset operations with pagination
- Optimizes queries for common access patterns
- Manages database resources efficiently
- Implements caching for frequently accessed data

## Error Handling
- Database connection errors → 500 Internal Server Error
- Constraint violations → 400 Bad Request or 409 Conflict
- Query errors → 500 Internal Server Error
- Timeout errors → 500 Internal Server Error
- Permission errors → 403 Forbidden
- Not found errors → 404 Not Found

## Quality Requirements
- Must handle database operations efficiently and safely
- Must maintain data consistency and integrity
- Must manage connections and resources properly
- Must handle concurrent database operations safely
- Must maintain security and privacy in operations
- Must provide proper error handling and logging