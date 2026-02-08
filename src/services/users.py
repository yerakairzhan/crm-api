# User service with business logic and JWT authentication

from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import os

from src.repositories.users import UserRepository
from src.schemas.users import UserCreate, UserUpdate, UserResponse, TokenData, UserLogin, Token
from src.models.users import User, UserRole

# Password hashing (pbkdf2_sha256 avoids bcrypt backend issues)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class UserService:
    # Service layer for user operations


    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Verify a password against its hash

        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        # Hash a password

        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        # Create JWT access token

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        # Create JWT refresh token

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> TokenData:
        # Verify JWT token and return token data

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            type_: str = payload.get("type")

            if user_id is None or type_ != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                )
            return TokenData(user_id=UUID(user_id), email=email)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        # Create a new user

        # Check if user already exists
        existing_user = UserRepository.get_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = UserService.get_password_hash(user.password)
        return UserRepository.create(db, user, hashed_password)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        # Authenticate a user

        user = UserRepository.get_by_email(db, email)
        if not user:
            return None
        if not UserService.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def login(db: Session, login_data: UserLogin) -> Token:
        # Login user and return access/refresh tokens

        user = UserService.authenticate_user(db, login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = UserService.create_access_token(
            {"sub": str(user.id), "email": user.email, "role": user.role}
        )
        refresh_token = UserService.create_refresh_token(
            {"sub": str(user.id), "email": user.email, "role": user.role}
        )

        # Store refresh token hash
        user.refresh_token_hash = UserService.get_password_hash(refresh_token)
        db.add(user)
        db.commit()
        db.refresh(user)

        return Token(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def refresh(db: Session, refresh_token: str) -> Token:
        # Refresh access token using refresh token

        token_data = UserService.verify_token(refresh_token, token_type="refresh")
        if not token_data.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user = UserRepository.get_by_id(db, token_data.user_id)
        if not user or not user.refresh_token_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        if not UserService.verify_password(refresh_token, user.refresh_token_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        access_token = UserService.create_access_token(
            {"sub": str(user.id), "email": user.email, "role": user.role}
        )
        new_refresh_token = UserService.create_refresh_token(
            {"sub": str(user.id), "email": user.email, "role": user.role}
        )

        user.refresh_token_hash = UserService.get_password_hash(new_refresh_token)
        db.add(user)
        db.commit()
        db.refresh(user)

        return Token(access_token=access_token, refresh_token=new_refresh_token)

    @staticmethod
    def get_user(db: Session, user_id: UUID) -> Optional[User]:
        # Get user by ID

        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        # Get all users

        return UserRepository.get_all(db, skip, limit)

    @staticmethod
    def update_user(db: Session, user_id: UUID, user_update: UserUpdate, current_user: User) -> User:
        # Update user

        # Spec does not restrict user updates beyond authentication

        hashed_password = None
        if user_update.password:
            hashed_password = UserService.get_password_hash(user_update.password)

        user = UserRepository.update(db, user_id, user_update, hashed_password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def delete_user(db: Session, user_id: UUID, current_user: User) -> bool:
        # Delete user

        # Spec does not restrict user deletes beyond authentication

        success = UserRepository.delete(db, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return success
