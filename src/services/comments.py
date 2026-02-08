"""
Comment service with business logic
"""
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status

from src.repositories.comments import CommentRepository
from src.repositories.tasks import TaskRepository
from src.schemas.comments import CommentCreate, CommentUpdate
from src.models.users import User, UserRole


class CommentService:
    """Service layer for comment operations"""

    @staticmethod
    def create_comment(db: Session, comment: CommentCreate, current_user: User):
        """Create a new comment (only AUTHOR role)"""
        if current_user.role != UserRole.AUTHOR:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only users with role 'author' can create comments",
            )

        task = TaskRepository.get_by_id(db, comment.task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return CommentRepository.create(db, comment, current_user.id)

    @staticmethod
    def get_all_comments(db: Session, skip: int = 0, limit: int = 100):
        """Get all comments sorted by date (newest first)"""
        return CommentRepository.get_all(db, skip, limit)

    @staticmethod
    def get_comments_by_task(db: Session, task_id: UUID, skip: int = 0, limit: int = 100):
        """Get comments for a task sorted by date (newest first)"""
        return CommentRepository.get_by_task(db, task_id, skip, limit)

    @staticmethod
    def get_comment(db: Session, comment_id: UUID):
        """Get comment by ID"""
        comment = CommentRepository.get_by_id(db, comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )
        return comment

    @staticmethod
    def update_comment(db: Session, comment_id: UUID, comment_update: CommentUpdate, current_user: User):
        """Update comment (only owner)"""
        comment = CommentRepository.get_by_id(db, comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

        if comment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own comments",
            )

        updated = CommentRepository.update(db, comment_id, comment_update)
        return updated

    @staticmethod
    def delete_comment(db: Session, comment_id: UUID, current_user: User) -> None:
        """Delete comment (only owner)"""
        comment = CommentRepository.get_by_id(db, comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

        if comment.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own comments",
            )

        CommentRepository.delete(db, comment_id)
