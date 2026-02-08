"""
Comment API endpoints
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from db import get_db
from src.schemas.comments import CommentCreate, CommentUpdate, CommentResponse
from src.services.comments import CommentService
from src.models.users import User
from src.api.users import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new comment (only AUTHOR role)"""
    return CommentService.create_comment(db, comment, current_user)


@router.get("/", response_model=List[CommentResponse])
def get_comments(
    task_id: Optional[UUID] = Query(None, description="Filter comments by task ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get comments sorted by date (newest first)"""
    if task_id:
        return CommentService.get_comments_by_task(db, task_id, skip, limit)
    return CommentService.get_all_comments(db, skip, limit)


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get comment by ID"""
    return CommentService.get_comment(db, comment_id)


@router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: UUID,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update comment (only owner)"""
    return CommentService.update_comment(db, comment_id, comment_update, current_user)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete comment (only owner)"""
    CommentService.delete_comment(db, comment_id, current_user)
    return None
