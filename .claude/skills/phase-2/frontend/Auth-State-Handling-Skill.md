# Auth State Handling Skill

## Purpose
Manage authentication state lifecycle in the frontend application, including detection, persistence, restoration, and state change reactions.

## Behavior Description
This skill provides a standardized approach to handling authentication state in the browser, ensuring consistent behavior across all authentication-related operations.

## Core Behaviors
- **State Detection**: Automatically detect whether a user is currently authenticated by checking for stored JWT tokens
- **Secure Persistence**: Safely store JWT tokens in browser storage (localStorage or sessionStorage) following security best practices
- **State Restoration**: Automatically restore authentication state when the application loads or page refreshes
- **Redirect Management**: Trigger appropriate navigation redirects when authentication state changes (e.g., redirect to dashboard when logged in, or to login when logged out)

## Scope
- **IN SCOPE**: Browser storage management, auth state detection, redirect triggering, state persistence
- **OUT OF SCOPE**: JWT validation, password processing, backend authentication logic, user credential verification

## Reusability
This skill can be applied across any Next.js page or component that needs to manage authentication state, ensuring consistent behavior regardless of the specific UI implementation.

## Constraints
- Must not validate JWT tokens or verify their authenticity
- Cannot handle credential processing or authentication business logic
- Limited to frontend authentication state management only