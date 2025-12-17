from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse, PaginatedUserResponse
from app.services.user_service import UserService
from app.config import get_settings

router = APIRouter(prefix="/users", tags=["users"])
settings = get_settings()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with all validations.
    
    - Validates email, mobile, Aadhaar, PAN formats
    - Ensures age >= 18 years
    - Prevents duplicate registrations
    - Rate limited: 100 requests per minute per IP (global default)
    - Supports idempotency_key to prevent duplicate submissions
    """
    return UserService.create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get a user by ID"""
    return UserService.get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user information.
    
    - Only provided fields are updated
    - Validates uniqueness constraints
    - Uses optimistic locking with version field
    """
    return UserService.update_user(db, user_id, user)

@router.get("/", response_model=PaginatedUserResponse)
def get_all_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get all users with pagination.
    
    - Default page size: 10
    - Maximum page size: 100
    - Returns total count and page info
    """
    return UserService.get_all_users(db, page, page_size)

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Soft delete a user.
    
    - User is marked as deleted but not removed from database
    - Allows data recovery and audit trail
    """
    return UserService.soft_delete_user(db, user_id)

@router.get("/search/", response_model=PaginatedUserResponse)
def search_users(
    request: Request,
    q: str = Query(..., min_length=2, description="Search query for name or email"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Search users by name or email.
    
    - Minimum 2 characters required
    - Searches in name and email fields
    - Returns paginated results
    - Rate limited: 100 requests per minute per IP (global default)
    """
    return UserService.search_users(db, q, page, page_size)