"""
Comment repository for database operations
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from src.models.comments import Comment
from src.schemas.comments import CommentCreate, CommentUpdate


class CommentRepository:
    """Repository for Comment CRUD operations"""

    @staticmethod
    def create(db: Session, comment: CommentCreate, user_id: UUID) -> Comment:
        """Create a new comment"""
        db_comment = Comment(
            task_id=comment.task_id,
            user_id=user_id,
            text=comment.text
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @staticmethod
    def get_by_id(db: Session, comment_id: UUID) -> Optional[Comment]:
        """Get comment by ID"""
        return db.query(Comment).filter(Comment.id == comment_id).first()

    @staticmethod
    def get_by_task(db: Session, task_id: UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get all comments for a task sorted by date (newest first)"""
        return db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get all comments sorted by date (newest first)"""
        return db.query(Comment).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, comment_id: UUID, comment_update: CommentUpdate) -> Optional[Comment]:
        """Update comment"""
        db_comment = CommentRepository.get_by_id(db, comment_id)
        if not db_comment:
            return None

        update_data = comment_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_comment, field, value)

        db.commit()
        db.refresh(db_comment)
        return db_comment

    @staticmethod
    def delete(db: Session, comment_id: UUID) -> bool:
        """Delete comment"""
        db_comment = CommentRepository.get_by_id(db, comment_id)
        if not db_comment:
            return False

        db.delete(db_comment)
        db.commit()
        return True