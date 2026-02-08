"""
Comment Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from uuid import UUID


class CommentBase(BaseModel):
    """Base comment schema"""
    text: str = Field(..., min_length=1, max_length=1000)

    @validator('text')
    def text_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Comment text cannot be empty')
        return v.strip()


class CommentCreate(CommentBase):
    """Schema for creating a comment"""
    task_id: UUID


class CommentUpdate(BaseModel):
    """Schema for updating a comment"""
    text: Optional[str] = Field(None, min_length=1, max_length=1000)

    @validator('text')
    def text_not_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Comment text cannot be empty')
        return v.strip() if v else v


class CommentResponse(CommentBase):
    """Schema for comment response"""
    id: UUID
    task_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True