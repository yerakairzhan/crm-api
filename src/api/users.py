# User API endpoints and auth dependencies

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from db import get_db
from src.schemas.users import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    RefreshTokenRequest,
)
from src.services.users import UserService
from src.repositories.users import UserRepository
from src.models.users import User

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    # Get current user from JWT access token

    token = credentials.credentials
    token_data = UserService.verify_token(token, token_type="access")
    if not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = UserRepository.get_by_id(db, token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Register a new user

    return UserService.create_user(db, user)


@router.post("/login", response_model=Token)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    # Login and return access/refresh tokens

    return UserService.login(db, login_data)


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    # Refresh access token

    return UserService.refresh(db, refresh_data.refresh_token)


@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get all users

    return UserService.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get user by ID

    return UserService.get_user(db, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Update user

    return UserService.update_user(db, user_id, user_update, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Delete user

    UserService.delete_user(db, user_id, current_user)
    return None
