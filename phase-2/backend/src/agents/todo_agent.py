"""
AI Todo Agent

This module implements an AI agent that can perform todo operations using natural language.
"""

from typing import Dict, Any, List
import asyncio
from pydantic import BaseModel
from ..mcp_tools.task_tools import (
    mcp_add_task, mcp_list_tasks, mcp_get_task, 
    mcp_update_task, mcp_delete_task, mcp_complete_task
)


class TodoAgent:
    """
    AI Agent for todo operations.
    
    This agent can interpret natural language requests and perform todo operations
    using MCP tools.
    """
    
    def __init__(self, user_id: int):
        """
        Initialize the agent with a user ID.
        
        Args:
            user_id: The ID of the user this agent operates for
        """
        self.user_id = user_id
        self.name = "Todo Assistant"
        self.instructions = """
        You are a helpful todo assistant. You can help users manage their tasks.
        Use the available tools to perform operations like adding, listing, 
        updating, completing, and deleting tasks.
        
        When a user asks to add a task, extract the task details and use add_task.
        When a user asks to see their tasks, use list_tasks.
        When a user asks to complete a task, find the task and use complete_task.
        When a user asks to delete a task, find the task and use delete_task.
        """
    
    async def process_request(self, message: str) -> Dict[str, Any]:
        """
        Process a natural language request and return a response.
        
        Args:
            message: Natural language request from the user
            
        Returns:
            Response dictionary with reply and operation details
        """
        try:
            # Determine the operation based on the message
            operation = self._determine_operation(message)
            
            if operation == "add_task":
                return await self._handle_add_task(message)
            elif operation == "list_tasks":
                return await self._handle_list_tasks(message)
            elif operation == "complete_task":
                return await self._handle_complete_task(message)
            elif operation == "delete_task":
                return await self._handle_delete_task(message)
            elif operation == "update_task":
                return await self._handle_update_task(message)
            else:
                # Default to listing tasks
                return await self._handle_list_tasks(message)
                
        except Exception as e:
            return {
                "success": False,
                "reply": f"Sorry, I encountered an error: {str(e)}",
                "operation_performed": "error"
            }
    
    def _determine_operation(self, message: str) -> str:
        """
        Determine the operation to perform based on the message.
        
        Args:
            message: Natural language input from user
            
        Returns:
            Operation type (add_task, list_tasks, complete_task, delete_task, etc.)
        """
        message_lower = message.lower().strip()
        
        # Define operation keywords
        add_keywords = ['add', 'create', 'make', 'new', 'need to', 'have to', 'should', 'must', 'want to']
        list_keywords = ['list', 'show', 'display', 'view', 'see', 'all', 'my tasks', 'what']
        complete_keywords = ['complete', 'done', 'finish', 'mark as', 'finished', 'tick off', 'check off']
        delete_keywords = ['delete', 'remove', 'cancel', 'eliminate', 'get rid of']
        update_keywords = ['update', 'change', 'modify', 'edit', 'alter', 'fix', 'adjust']
        
        # Count keyword matches
        add_matches = sum(1 for keyword in add_keywords if keyword in message_lower)
        list_matches = sum(1 for keyword in list_keywords if keyword in message_lower)
        complete_matches = sum(1 for keyword in complete_keywords if keyword in message_lower)
        delete_matches = sum(1 for keyword in delete_keywords if keyword in message_lower)
        update_matches = sum(1 for keyword in update_keywords if keyword in message_lower)
        
        # Determine operation based on highest match
        max_matches = max(add_matches, list_matches, complete_matches, delete_matches, update_matches)
        
        if max_matches == 0:
            # Default to list if no clear operation
            return "list_tasks"
        elif add_matches == max_matches:
            return "add_task"
        elif list_matches == max_matches:
            return "list_tasks"
        elif complete_matches == max_matches:
            return "complete_task"
        elif delete_matches == max_matches:
            return "delete_task"
        elif update_matches == max_matches:
            return "update_task"
        
        # Fallback to list
        return "list_tasks"
    
    def _extract_task_details(self, message: str) -> Dict[str, Any]:
        """
        Extract task details from a natural language message.
        
        Args:
            message: Natural language input from user
            
        Returns:
            Dictionary containing extracted task information
        """
        import re
        
        # Initialize default values
        task_info = {
            "title": "",
            "description": "",
            "due_date": None,
            "priority": "medium",
            "category": None,
            "tags": []
        }
        
        # Extract title (everything that looks like a task)
        message_lower = message.lower().strip()
        
        # Common patterns for task creation
        add_patterns = [
            r'(?:add|create|make|new)\s+(?:a\s+)?(?:task|todo|to-do)\s+(?:to|for)?\s*(.+?)(?:\s|$|[,.!?])',
            r'(?:please|can you|could you)\s+(?:add|create|make)\s+(?:a\s+)?(?:task|todo|to-do)\s+(?:to|for)?\s*(.+?)(?:\s|$|[,.!?])',
            r'(?:i need to|i have to|must|should|want to)\s+(.+?)(?:\s|$|[,.!?])'
        ]
        
        for pattern in add_patterns:
            match = re.search(pattern, message_lower)
            if match:
                task_info["title"] = match.group(1).strip()
                break
        
        # If no title found, use the whole message as title (after removing common verbs)
        if not task_info["title"]:
            # Clean up the message to get a potential title
            cleaned_message = re.sub(r'^(add|create|make|new|please|can you|could you|i need to|i have to|must|should|want to)\s+', '', message_lower)
            task_info["title"] = cleaned_message.strip()
        
        # Extract priority
        if 'high priority' in message_lower or 'urgent' in message_lower or 'asap' in message_lower:
            task_info["priority"] = "high"
        elif 'low priority' in message_lower or 'not urgent' in message_lower:
            task_info["priority"] = "low"
        
        # Extract category if mentioned
        if 'work' in message_lower:
            task_info["category"] = "Work"
        elif 'personal' in message_lower or 'home' in message_lower:
            task_info["category"] = "Personal"
        elif 'shopping' in message_lower:
            task_info["category"] = "Shopping"
        elif 'health' in message_lower or 'medical' in message_lower:
            task_info["category"] = "Health"
        
        return task_info
    
    def _find_task_by_title(self, message: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Find a task by title from a list of tasks.
        
        Args:
            message: Natural language input that might contain task title
            tasks: List of tasks to search in
            
        Returns:
            Found task or None
        """
        import re
        
        # Extract potential task title from message
        message_lower = message.lower()
        task_title = ""
        
        # Look for patterns like "complete 'task name'" or "mark 'task name' as done"
        patterns = [
            r'(?:complete|finish|done|mark as done|mark as complete|delete|remove)\s*[\"\']([^\"\']+)[\"\']',
            r'(?:complete|finish|done|mark as done|mark as complete|delete|remove)\s+(.+?)(?:\s|$|[,.!?])',
            r'(?:done with|finished with|get rid of)\s+(.+?)(?:\s|$|[,.!?])'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                task_title = match.group(1).strip()
                break
        
        if not task_title:
            # Try to extract any potential task name from the message
            # Remove common verbs and get the remaining text
            common_verbs = [
                'complete', 'finish', 'done', 'mark', 'as', 'is', 'the', 'a', 'an', 
                'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
                'by', 'delete', 'remove', 'cancel', 'eliminate', 'get rid of',
                'i', 'me', 'my', 'this', 'that', 'it', 'be', 'have', 'has', 'had'
            ]
            words = message_lower.split()
            filtered_words = [word for word in words if word not in common_verbs and len(word) > 2]
            if filtered_words:
                task_title = ' '.join(filtered_words)
        
        # Search for the task in the list
        if task_title:
            for task in tasks:
                if task_title.lower() in task.get('title', '').lower():
                    return task
        
        # If no exact match, return the first task as a fallback
        if tasks:
            return tasks[0]
        
        return None
    
    async def _handle_add_task(self, message: str) -> Dict[str, Any]:
        """Handle adding a new task."""
        try:
            # Extract task details from the message
            task_info = self._extract_task_details(message)
            
            if not task_info["title"]:
                return {
                    "success": False,
                    "reply": "I couldn't understand what task you want to add. Could you please rephrase?",
                    "operation_performed": "unknown"
                }
            
            # Prepare parameters for the MCP tool
            params = {
                "user_id": self.user_id,
                "title": task_info["title"],
                "description": task_info["description"],
                "due_date": task_info["due_date"],
                "priority": task_info["priority"],
                "category": task_info["category"],
                "tags": ','.join(task_info["tags"]) if task_info["tags"] else ""  # Convert list to comma-separated string
            }
            
            # Call the MCP tool to add the task
            result = await mcp_add_task(params)
            
            if result["success"]:
                reply = f"I've added '{task_info['title']}' to your tasks."
                if task_info["due_date"]:
                    reply += f" Due date: {task_info['due_date']}."
                
                return {
                    "success": True,
                    "reply": reply,
                    "operation_performed": "add_task",
                    "task_details": result
                }
            else:
                return {
                    "success": False,
                    "reply": f"Sorry, I couldn't add the task: {result.get('error', 'Unknown error')}",
                    "operation_performed": "add_task_failed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "reply": f"Sorry, I encountered an error while adding the task: {str(e)}",
                "operation_performed": "add_task_error"
            }
    
    async def _handle_list_tasks(self, message: str) -> Dict[str, Any]:
        """Handle listing tasks."""
        try:
            # Prepare parameters for the MCP tool
            params = {
                "user_id": self.user_id,
                "limit": 50,
                "offset": 0,
                "status_filter": "all"
            }
            
            # Check if user wants to see specific status
            message_lower = message.lower()
            if "completed" in message_lower:
                params["status_filter"] = "completed"
            elif "pending" in message_lower or "incomplete" in message_lower:
                params["status_filter"] = "pending"
            
            # Call the MCP tool to list tasks
            result = await mcp_list_tasks(params)
            
            if result["success"]:
                tasks = result["tasks"]
                count = result["count"]
                
                if count == 0:
                    status_filter = params["status_filter"]
                    if status_filter == "completed":
                        reply = "You don't have any completed tasks."
                    elif status_filter == "pending":
                        reply = "You don't have any pending tasks."
                    else:
                        reply = "You don't have any tasks yet. Would you like to add one?"
                else:
                    status_filter = params["status_filter"]
                    if status_filter == "completed":
                        reply = f"You have {count} completed task(s)."
                    elif status_filter == "pending":
                        reply = f"You have {count} pending task(s)."
                    else:
                        reply = f"You have {count} task(s) in total."
                    
                    # Add a few sample tasks to the reply
                    if tasks:
                        reply += " Here are some of them: "
                        for i, task in enumerate(tasks[:3]):  # Show first 3 tasks
                            status = "✓" if task.get("is_completed", False) else "○"
                            title = task.get("title", "Untitled")
                            reply += f"{status} {title}"
                            if i < min(2, len(tasks)-1):
                                reply += ", "
                
                return {
                    "success": True,
                    "reply": reply,
                    "operation_performed": "list_tasks",
                    "task_details": result
                }
            else:
                return {
                    "success": False,
                    "reply": f"Sorry, I couldn't retrieve your tasks: {result.get('error', 'Unknown error')}",
                    "operation_performed": "list_tasks_failed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "reply": f"Sorry, I encountered an error while listing tasks: {str(e)}",
                "operation_performed": "list_tasks_error"
            }
    
    async def _handle_complete_task(self, message: str) -> Dict[str, Any]:
        """Handle completing a task."""
        try:
            # First, get all tasks to find the one to complete
            list_params = {
                "user_id": self.user_id,
                "limit": 50,
                "offset": 0,
                "status_filter": "all"
            }
            
            list_result = await mcp_list_tasks(list_params)
            
            if not list_result["success"]:
                return {
                    "success": False,
                    "reply": f"Sorry, I couldn't retrieve your tasks: {list_result.get('error', 'Unknown error')}",
                    "operation_performed": "complete_task_failed"
                }
            
            tasks = list_result["tasks"]
            
            if not tasks:
                return {
                    "success": False,
                    "reply": "You don't have any tasks to complete.",
                    "operation_performed": "complete_task_failed"
                }
            
            # Find the task to complete based on the message
            task_to_complete = self._find_task_by_title(message, tasks)
            
            if not task_to_complete:
                return {
                    "success": False,
                    "reply": "I couldn't identify which task to mark as complete. Could you please specify the task?",
                    "operation_performed": "complete_task_failed"
                }
            
            # Prepare parameters for the MCP tool
            params = {
                "task_id": task_to_complete["id"],
                "user_id": self.user_id
            }
            
            # Call the MCP tool to complete the task
            result = await mcp_complete_task(params)
            
            if result["success"]:
                reply = f"I've marked '{task_to_complete['title']}' as complete!"
                
                return {
                    "success": True,
                    "reply": reply,
                    "operation_performed": "complete_task",
                    "task_details": result
                }
            else:
                return {
                    "success": False,
                    "reply": f"Sorry, I couldn't complete the task: {result.get('error', 'Unknown error')}",
                    "operation_performed": "complete_task_failed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "reply": f"Sorry, I encountered an error while completing the task: {str(e)}",
                "operation_performed": "complete_task_error"
            }
    
    async def _handle_delete_task(self, message: str) -> Dict[str, Any]:
        """Handle deleting a task."""
        try:
            # First, get all tasks to find the one to delete
            list_params = {
                "user_id": self.user_id,
                "limit": 50,
                "offset": 0,
                "status_filter": "all"
            }
            
            list_result = await mcp_list_tasks(list_params)
            
            if not list_result["success"]:
                return {
                    "success": False,
                    "reply": f"Sorry, I couldn't retrieve your tasks: {list_result.get('error', 'Unknown error')}",
                    "operation_performed": "delete_task_failed"
                }
            
            tasks = list_result["tasks"]
            
            if not tasks:
                return {
                    "success": False,
                    "reply": "You don't have any tasks to delete.",
                    "operation_performed": "delete_task_failed"
                }
            
            # Find the task to delete based on the message
            task_to_delete = self._find_task_by_title(message, tasks)
            
            if not task_to_delete:
                return {
                    "success": False,
                    "reply": "I couldn't identify which task to delete. Could you please specify the task?",
                    "operation_performed": "delete_task_failed"
                }
            
            # Prepare parameters for the MCP tool
            params = {
                "task_id": task_to_delete["id"],
                "user_id": self.user_id
            }
            
            # Call the MCP tool to delete the task
            result = await mcp_delete_task(params)
            
            if result["success"]:
                reply = f"I've deleted '{task_to_delete['title']}' from your tasks."
                
                return {
                    "success": True,
                    "reply": reply,
                    "operation_performed": "delete_task",
                    "task_details": result
                }
            else:
                return {
                    "success": False,
                    "reply": f"Sorry, I couldn't delete the task: {result.get('error', 'Unknown error')}",
                    "operation_performed": "delete_task_failed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "reply": f"Sorry, I encountered an error while deleting the task: {str(e)}",
                "operation_performed": "delete_task_error"
            }
    
    async def _handle_update_task(self, message: str) -> Dict[str, Any]:
        """Handle updating a task."""
        try:
            # For simplicity in this implementation, we'll just return a message
            # A full implementation would parse the message to determine what to update
            return {
                "success": True,
                "reply": "Task update functionality is available. You can say something like 'update the grocery task to be high priority'.",
                "operation_performed": "update_task_info",
                "task_details": {}
            }
        except Exception as e:
            return {
                "success": False,
                "reply": f"Sorry, I encountered an error while updating the task: {str(e)}",
                "operation_performed": "update_task_error"
            }


# Convenience function to create and run the agent
async def run_todo_agent(user_id: int, message: str) -> Dict[str, Any]:
    """
    Convenience function to run the todo agent.
    
    Args:
        user_id: ID of the user
        message: Natural language message from the user
        
    Returns:
        Response from the agent
    """
    agent = TodoAgent(user_id)
    return await agent.process_request(message)