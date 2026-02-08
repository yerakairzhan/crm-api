"""
Task service with business logic
"""
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from typing import List

from src.repositories.tasks import TaskRepository
from src.schemas.tasks import TaskCreate, TaskUpdate
from src.models.users import User, UserRole


class TaskService:
    """Service layer for task operations"""

    @staticmethod
    def create_task(db: Session, task: TaskCreate, current_user: User):
        """Create a new task (only USER role)"""
        if current_user.role != UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only users with role 'user' can create tasks",
            )

        db_task = TaskRepository.create(db, task, current_user.id)

        # Auto-assign user's task_id to last created task
        current_user.task_id = db_task.id
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

        return db_task

    @staticmethod
    def get_all_tasks(db: Session, skip: int = 0, limit: int = 100):
        """Get all tasks sorted by date (newest first)"""
        return TaskRepository.get_all(db, skip, limit)

    @staticmethod
    def get_task(db: Session, task_id: UUID):
        """Get task by ID"""
        task = TaskRepository.get_by_id(db, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return task

    @staticmethod
    def update_task(db: Session, task_id: UUID, task_update: TaskUpdate, current_user: User):
        """Update task (only owner)"""
        task = TaskRepository.get_by_id(db, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        if task.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own tasks",
            )

        updated = TaskRepository.update(db, task_id, task_update)
        return updated

    @staticmethod
    def delete_task(db: Session, task_id: UUID, current_user: User) -> None:
        """Delete task (only owner)"""
        task = TaskRepository.get_by_id(db, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        if task.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own tasks",
            )

        TaskRepository.delete(db, task_id)
