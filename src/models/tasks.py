"""
Task SQLAlchemy model
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from db import UUIDType
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from db import Base


class Task(Base):
    """Task model"""
    __tablename__ = "tasks"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType, ForeignKey("users.id"), nullable=False)
    description = Column(String(1000), nullable=False)
    comment = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="tasks", foreign_keys=[user_id])
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
