# Task Pydantic schemas for request/response validation

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class TaskBase(BaseModel):
    # Base task schema

    description: str = Field(..., min_length=1, max_length=1000)
    comment: str = Field(..., min_length=1, max_length=1000)

    @field_validator('description')
    @classmethod
    def description_not_empty(cls, v: str):
        if not v or not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()

    @field_validator('comment')
    @classmethod
    def comment_not_empty(cls, v: str):
        if not v or not v.strip():
            raise ValueError('Comment cannot be empty')
        return v.strip()


class TaskCreate(TaskBase):
    # Schema for creating a task

    pass


class TaskUpdate(BaseModel):
    # Schema for updating a task

    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    comment: Optional[str] = Field(None, min_length=1, max_length=1000)

    @field_validator('description')
    @classmethod
    def description_not_empty(cls, v: Optional[str]):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Description cannot be empty')
        return v.strip() if v else v

    @field_validator('comment')
    @classmethod
    def comment_not_empty(cls, v: Optional[str]):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Comment cannot be empty')
        return v.strip() if v else v


class TaskResponse(TaskBase):
    # Schema for task response

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskWithComments(TaskResponse):
    # Schema for task with comments

    comments: List['CommentResponse'] = []

    model_config = ConfigDict(from_attributes=True)


# Import to avoid circular dependency
from src.schemas.comments import CommentResponse
TaskWithComments.model_rebuild()
