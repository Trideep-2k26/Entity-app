from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from typing import Optional
import uuid
from datetime import datetime

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            if not existing_email.is_deleted:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
            else:
                existing_email.is_deleted = False
                existing_email.deleted_at = None
                existing_email.deleted_by = None
                existing_email.is_active = True
                existing_email.name = user_data.name
                existing_email.primary_mobile = user_data.primary_mobile
                existing_email.secondary_mobile = user_data.secondary_mobile
                existing_email.aadhaar = user_data.aadhaar
                existing_email.pan = user_data.pan
                existing_email.date_of_birth = user_data.date_of_birth
                existing_email.place_of_birth = user_data.place_of_birth
                existing_email.current_address = user_data.current_address
                existing_email.permanent_address = user_data.permanent_address
                existing_email.version = str(uuid.uuid4())
                db.commit()
                db.refresh(existing_email)
                return existing_email
        
        existing_mobile = db.query(User).filter(User.primary_mobile == user_data.primary_mobile).first()
        if existing_mobile and not existing_mobile.is_deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mobile number already registered")
        
        existing_aadhaar = db.query(User).filter(User.aadhaar == user_data.aadhaar).first()
        if existing_aadhaar and not existing_aadhaar.is_deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aadhaar already registered")
        
        existing_pan = db.query(User).filter(User.pan == user_data.pan).first()
        if existing_pan and not existing_pan.is_deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PAN already registered")
        
        try:
            db_user = User(**user_data.model_dump())
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            db.rollback()
            error_msg = str(e.orig)
            if 'email' in error_msg:
                detail = "Email already exists in database"
            elif 'primary_mobile' in error_msg:
                detail = "Mobile number already exists in database"
            elif 'aadhaar' in error_msg:
                detail = "Aadhaar already exists in database"
            elif 'pan' in error_msg:
                detail = "PAN already exists in database"
            else:
                detail = "Duplicate entry found"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        user = db.query(User).filter(and_(User.id == user_id, User.is_deleted == False)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: str, user_data: UserUpdate) -> User:
        db_user = UserService.get_user_by_id(db, user_id)
        update_data = user_data.model_dump(exclude_unset=True)
        
        if 'email' in update_data and update_data['email'] != db_user.email:
            if db.query(User).filter(and_(User.email == update_data['email'], User.is_deleted == False, User.id != user_id)).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        
        if 'primary_mobile' in update_data and update_data['primary_mobile'] != db_user.primary_mobile:
            if db.query(User).filter(and_(User.primary_mobile == update_data['primary_mobile'], User.is_deleted == False, User.id != user_id)).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mobile number already in use")
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db_user.version = str(uuid.uuid4())
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_all_users(db: Session, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        total = db.query(User).filter(User.is_deleted == False).count()
        users = db.query(User).filter(User.is_deleted == False)\
            .order_by(User.created_at.desc())\
            .offset(offset)\
            .limit(page_size)\
            .all()
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
        db_user = UserService.get_user_by_id(db, user_id)
        db_user.is_deleted = True
        db_user.deleted_at = datetime.utcnow()
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
        return db_user