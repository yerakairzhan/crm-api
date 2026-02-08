# User SQLAlchemy model

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from db import UUIDType
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from db import Base


class UserRole(str, enum.Enum):
    # User role enumeration

    AUTHOR = "author"
    USER = "user"


class User(Base):
    # User model for authentication and task management

    __tablename__ = "users"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)  # Hashed password
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    task_id = Column(UUIDType, ForeignKey("tasks.id"), nullable=True)
    refresh_token_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="Task.user_id",
    )
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    # Optional link to last created task
    last_task = relationship("Task", foreign_keys=[task_id], uselist=False)
