"""
MCP (Model Context Protocol) tools for task operations.

This module implements tools that expose task operations to AI agents via MCP.
"""

from typing import Dict, List, Optional, Any
from sqlmodel import Session
from pydantic import BaseModel
from ..database import get_session, engine
from ..services.task_service import TaskService
from ..models.task import TaskCreate, TaskUpdate
from ..middleware.auth_middleware import auth_middleware


class TaskCreateRequest(BaseModel):
    """Request model for creating a task."""
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = "medium"
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    user_id: int


class TaskUpdateRequest(BaseModel):
    """Request model for updating a task."""
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    user_id: int


class TaskDeleteRequest(BaseModel):
    """Request model for deleting a task."""
    task_id: int
    user_id: int


class TaskGetRequest(BaseModel):
    """Request model for getting a task."""
    task_id: int
    user_id: int


class TaskListRequest(BaseModel):
    """Request model for listing tasks."""
    user_id: int
    limit: int = 50
    offset: int = 0
    status_filter: str = "all"  # "all", "pending", "completed"


class TaskToolProvider:
    """Provider class for task-related MCP tools."""
    
    def __init__(self):
        pass
    
    async def add_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new task.
        
        Args:
            params: Parameters for task creation including title, description, etc.
            
        Returns:
            Result of the operation
        """
        try:
            # Extract parameters
            user_id = params.get('user_id')
            title = params.get('title')
            description = params.get('description', '')
            due_date = params.get('due_date')
            priority = params.get('priority', 'medium')
            category = params.get('category')
            tags = params.get('tags', [])
            
            if not user_id or not title:
                return {
                    "success": False,
                    "error": "user_id and title are required"
                }
            
            # Create task using the service
            from ..database import Session
            with Session(engine) as session:
                task_create = TaskCreate(
                    title=title,
                    description=description,
                    due_date=due_date,
                    priority=priority,
                    category=category,
                    tags=tags
                )
                
                task = TaskService.create_task(session, task_create, user_id)
                
                return {
                    "success": True,
                    "task_id": task.id,
                    "title": task.title,
                    "message": f"Task '{task.title}' has been added successfully"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List tasks for a user.
        
        Args:
            params: Parameters for task listing including user_id, filters, etc.
            
        Returns:
            List of tasks
        """
        try:
            user_id = params.get('user_id')
            limit = params.get('limit', 50)
            offset = params.get('offset', 0)
            status_filter = params.get('status_filter', 'all')
            
            if not user_id:
                return {
                    "success": False,
                    "error": "user_id is required"
                }
            
            from ..database import Session
            with Session(engine) as session:
                tasks = TaskService.get_tasks_for_user(
                    session, user_id, limit, offset, status_filter
                )
                
                # Convert tasks to dictionaries
                task_list = []
                for task in tasks:
                    task_dict = {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None,
                        "due_date": task.due_date,
                        "priority": task.priority,
                        "category": task.category,
                        "tags": task.tags.split(',') if task.tags else []
                    }
                    task_list.append(task_dict)
                
                return {
                    "success": True,
                    "tasks": task_list,
                    "count": len(task_list)
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a specific task by ID.
        
        Args:
            params: Parameters including task_id and user_id
            
        Returns:
            Task details
        """
        try:
            task_id = params.get('task_id')
            user_id = params.get('user_id')
            
            if not task_id or not user_id:
                return {
                    "success": False,
                    "error": "task_id and user_id are required"
                }
            
            from ..database import Session
            with Session(engine) as session:
                task = TaskService.get_task_by_id(session, task_id, user_id)
                
                if not task:
                    return {
                        "success": False,
                        "error": "Task not found or access denied"
                    }
                
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "due_date": task.due_date,
                    "priority": task.priority,
                    "category": task.category,
                    "tags": task.tags.split(',') if task.tags else []
                }
                
                return {
                    "success": True,
                    "task": task_dict
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def update_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a specific task.
        
        Args:
            params: Parameters for task update including task_id, user_id, and fields to update
            
        Returns:
            Result of the operation
        """
        try:
            task_id = params.get('task_id')
            user_id = params.get('user_id')
            
            if not task_id or not user_id:
                return {
                    "success": False,
                    "error": "task_id and user_id are required"
                }
            
            # Prepare update object with provided fields
            update_data = {}
            for field in ['title', 'description', 'is_completed', 'due_date', 'priority', 'category', 'tags']:
                if field in params:
                    update_data[field] = params[field]
            
            if not update_data:
                return {
                    "success": False,
                    "error": "At least one field to update is required"
                }
            
            from ..database import Session
            with Session(engine) as session:
                task_update = TaskUpdate(**update_data)
                updated_task = TaskService.update_task(session, task_id, task_update, user_id)
                
                if not updated_task:
                    return {
                        "success": False,
                        "error": "Task not found or access denied"
                    }
                
                return {
                    "success": True,
                    "task_id": updated_task.id,
                    "message": f"Task '{updated_task.title}' has been updated successfully"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def delete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a specific task.
        
        Args:
            params: Parameters including task_id and user_id
            
        Returns:
            Result of the operation
        """
        try:
            task_id = params.get('task_id')
            user_id = params.get('user_id')
            
            if not task_id or not user_id:
                return {
                    "success": False,
                    "error": "task_id and user_id are required"
                }
            
            from ..database import Session
            with Session(engine) as session:
                success = TaskService.delete_task(session, task_id, user_id)
                
                if not success:
                    return {
                        "success": False,
                        "error": "Task not found or access denied"
                    }
                
                return {
                    "success": True,
                    "message": "Task has been deleted successfully"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def complete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mark a task as completed.
        
        Args:
            params: Parameters including task_id and user_id
            
        Returns:
            Result of the operation
        """
        try:
            task_id = params.get('task_id')
            user_id = params.get('user_id')
            
            if not task_id or not user_id:
                return {
                    "success": False,
                    "error": "task_id and user_id are required"
                }
            
            from ..database import Session
            with Session(engine) as session:
                updated_task = TaskService.toggle_task_completion(session, task_id, user_id)
                
                if not updated_task:
                    return {
                        "success": False,
                        "error": "Task not found or access denied"
                    }
                
                status = "completed" if updated_task.is_completed else "marked as pending"
                return {
                    "success": True,
                    "task_id": updated_task.id,
                    "message": f"Task '{updated_task.title}' has been {status}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global instance of the tool provider
task_tool_provider = TaskToolProvider()


# Functions that can be called by the MCP server
async def mcp_add_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP wrapper for adding a task."""
    return await task_tool_provider.add_task(params)


async def mcp_list_tasks(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP wrapper for listing tasks."""
    return await task_tool_provider.list_tasks(params)


async def mcp_get_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP wrapper for getting a task."""
    return await task_tool_provider.get_task(params)


async def mcp_update_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP wrapper for updating a task."""
    return await task_tool_provider.update_task(params)


async def mcp_delete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP wrapper for deleting a task."""
    return await task_tool_provider.delete_task(params)


async def mcp_complete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """MCP wrapper for completing a task."""
    return await task_tool_provider.complete_task(params)