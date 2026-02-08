"""
Main application module.

This module creates the FastAPI application and sets up all routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Import routers
from src.api.auth_router import auth_router
from src.api.task_router import task_router
from src.api.ai_todo_router import ai_todo_router
from src.database import create_tables

# Load environment variables - try local file first, then default
load_dotenv('.env.local')
load_dotenv('.env')

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="A secure todo application with JWT authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(ai_todo_router)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_tables()

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Todo API is running"}

# Root endpoint
@app.get("/api/health")
def api_health():
    return {"status": "ok", "service": "todo-api"}