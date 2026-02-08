# Auth API endpoints (aliases for /users/*)

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from src.schemas.users import UserCreate, UserLogin, Token, RefreshTokenRequest, UserResponse
from src.services.users import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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
