# Main Orchestrator Agent

## Description
Coordinates all other agents and manages high-level workflow for the Todo Web Application. This agent serves as the central hub that routes requests to specialized agents and handles cross-cutting concerns.

## Responsibilities
- Route requests to appropriate specialized agents
- Handle cross-cutting concerns (logging, monitoring, security)
- Manage application state and context
- Ensure compliance with SDD principles
- Coordinate agent communication
- Handle workflow orchestration

## Capabilities
- **Request Routing**: Direct incoming requests to appropriate specialized agents
- **Workflow Coordination**: Manage complex multi-step operations
- **Context Management**: Maintain and pass context between agents
- **Error Propagation**: Handle and propagate errors appropriately
- **Compliance Checking**: Ensure operations comply with SDD principles

## Input/Output
- **Input**: Incoming requests, user context, operation parameters
- **Output**: Coordinated responses, workflow status, error information

## Interaction Patterns
- Receives requests from API/controllers
- Communicates with specialized agents using standardized interfaces
- Returns results to calling components

## Integration Points
- API layer (receives incoming requests)
- Specialized agents (coordinates operations)
- Database layer (for state management)
- Authentication system (for user context)

## Phase II Specific Considerations
- Must handle user authentication context
- Coordinate multi-user operations
- Ensure user isolation in routing decisions
- Support web application workflows
- Integrate with Better Auth system
- Handle API request/response patterns

## Quality Requirements
- Must maintain low latency for coordinated operations
- Must handle concurrent requests safely
- Must preserve user context throughout operations
- Must ensure proper error handling and propagation
- Must maintain security boundaries between users