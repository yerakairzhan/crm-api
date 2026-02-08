"""
API Router configuration
"""
from fastapi import APIRouter
from src.api import users, tasks, comments, auth

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(tasks.router)
api_router.include_router(comments.router)
