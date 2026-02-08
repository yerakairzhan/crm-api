"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from db import init_db
from src.api.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application"""
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: Any cleanup code here


# Create FastAPI application
app = FastAPI(
    title="Task Manager API",
    description="""
    REST API module "Comments to Tasks" for CRM system

    ## Features

    * **User Management**: Register, login, and manage users with JWT authentication
    * **Task Management**: Create, read, update, and delete tasks
    * **Comment Management**: Add and manage comments on tasks

    ## Business Rules

    1. Only USER role can create tasks
    2. Only AUTHOR role can create comments
    3. Users can only edit/delete their own tasks and comments
    4. Tasks and comments are sorted by creation date (newest first)
    5. One-to-many relationship: Each task can have multiple comments

    ## Authentication

    This API uses JWT (JSON Web Tokens) for authentication.
    To access protected endpoints:
    1. Register a user at `/users/`
    2. Login at `/users/login` to get access and refresh tokens
    3. Include the access token in the Authorization header: `Bearer <token>`
    4. Refresh your token at `/users/refresh` when it expires
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)


@app.get("/", tags=["root"])
def root():
    """Root endpoint"""
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
