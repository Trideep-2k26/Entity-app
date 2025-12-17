from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from typing import Optional
import uuid
from datetime import datetime

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user with validation"""
        # Check for duplicate email
        if db.query(User).filter(and_(User.email == user_data.email, User.is_deleted == False)).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check for duplicate mobile
        if db.query(User).filter(and_(User.primary_mobile == user_data.primary_mobile, User.is_deleted == False)).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mobile number already registered"
            )
        
        # Check for duplicate Aadhaar
        if db.query(User).filter(and_(User.aadhaar == user_data.aadhaar, User.is_deleted == False)).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aadhaar already registered"
            )
        
        # Check for duplicate PAN
        if db.query(User).filter(and_(User.pan == user_data.pan, User.is_deleted == False)).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PAN already registered"
            )
        
        # Create user
        db_user = User(**user_data.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID (excluding soft deleted)"""
        user = db.query(User).filter(and_(User.id == user_id, User.is_deleted == False)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: str, user_data: UserUpdate) -> User:
        """Update user with optimistic locking"""
        db_user = UserService.get_user_by_id(db, user_id)
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        # Check for duplicate email if being updated
        if 'email' in update_data and update_data['email'] != db_user.email:
            if db.query(User).filter(and_(User.email == update_data['email'], User.is_deleted == False, User.id != user_id)).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
        
        # Check for duplicate mobile if being updated
        if 'primary_mobile' in update_data and update_data['primary_mobile'] != db_user.primary_mobile:
            if db.query(User).filter(and_(User.primary_mobile == update_data['primary_mobile'], User.is_deleted == False, User.id != user_id)).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Mobile number already in use"
                )
        
        # Update fields
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        # Update version for optimistic locking
        db_user.version = str(uuid.uuid4())
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_all_users(db: Session, page: int = 1, page_size: int = 10):
        """Get all users with pagination"""
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Get total count
        total = db.query(User).filter(User.is_deleted == False).count()
        
        # Get paginated users
        users = db.query(User).filter(User.is_deleted == False)\
            .order_by(User.created_at.desc())\
            .offset(offset)\
            .limit(page_size)\
            .all()
        
        # Calculate total pages
        total_pages = (total + page_size - 1) // page_size
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "data": users
        }
    
    @staticmethod
    def soft_delete_user(db: Session, user_id: str) -> User:
        """Soft delete a user"""
        db_user = UserService.get_user_by_id(db, user_id)
        db_user.is_deleted = True
        db_user.deleted_at = datetime.utcnow()
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
        return db_user