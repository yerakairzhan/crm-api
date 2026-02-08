# Task repository for database operations

from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from src.models.tasks import Task
from src.models.comments import Comment
from src.models.users import User
from src.schemas.tasks import TaskCreate, TaskUpdate


class TaskRepository:
    # Repository for Task CRUD operations


    @staticmethod
    def create(db: Session, task: TaskCreate, user_id: UUID) -> Task:
        # Create a new task

        db_task = Task(
            user_id=user_id,
            description=task.description,
            comment=task.comment,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_by_id(db: Session, task_id: UUID) -> Optional[Task]:
        # Get task by ID

        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        # Get all tasks sorted by date (newest first)

        return db.query(Task).order_by(Task.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_user(db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Task]:
        # Get all tasks for a specific user

        return db.query(Task).filter(Task.user_id == user_id).order_by(Task.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        # Update task

        db_task = TaskRepository.get_by_id(db, task_id)
        if not db_task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete(db: Session, task_id: UUID) -> bool:
        # Delete task

        db_task = TaskRepository.get_by_id(db, task_id)
        if not db_task:
            return False

        # Ensure comments are removed first to avoid FK issues in SQLite
        db.query(Comment).filter(Comment.task_id == task_id).delete()
        # Clear last_task reference for users that point to this task
        db.query(User).filter(User.task_id == task_id).update({User.task_id: None})
        db.delete(db_task)
        db.commit()
        return True
