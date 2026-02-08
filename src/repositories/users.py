"""
User repository for database operations
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from src.models.users import User
from src.schemas.users import UserCreate, UserUpdate


class UserRepository:
    """Repository for User CRUD operations"""

    @staticmethod
    def create(db: Session, user: UserCreate, hashed_password: str) -> User:
        """Create a new user"""
        db_user = User(
            email=user.email,
            password=hashed_password,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, user_id: UUID, user_update: UserUpdate, hashed_password: Optional[str] = None) -> Optional[
        User]:
        """Update user"""
        db_user = UserRepository.get_by_id(db, user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        # Handle password separately if provided
        if hashed_password:
            update_data['password'] = hashed_password
        elif 'password' in update_data:
            del update_data['password']

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete(db: Session, user_id: UUID) -> bool:
        """Delete user"""
        db_user = UserRepository.get_by_id(db, user_id)
        if not db_user:
            return False

        db.delete(db_user)
        db.commit()
        return True