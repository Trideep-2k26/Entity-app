from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from typing import List, Tuple
import uuid
from datetime import datetime
import logging
import hashlib
from app.config import get_settings

logger = logging.getLogger(__name__)

class UserService:
    
    @staticmethod
    def _hash_pii(value: str) -> str:
        """Create a non-reversible hash of PII for secure logging."""
        settings = get_settings()
        hash_input = f"{settings.LOG_HASH_SECRET}{value}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()[:16]
    
    @staticmethod
    def _check_unique_fields(db: Session, user_data: UserCreate, exclude_id: str = None) -> None:
        checks: List[Tuple[str, str, str]] = [
            ('email', user_data.email, "Email"),
            ('primary_mobile', user_data.primary_mobile, "Mobile number"),
            ('aadhaar', user_data.aadhaar, "Aadhaar"),
            ('pan', user_data.pan, "PAN"),
        ]
        
        for field, value, name in checks:
            query = db.query(User).filter(
                getattr(User, field) == value,
                User.is_deleted == False
            )
            if exclude_id:
                query = query.filter(User.id != exclude_id)
            
            if query.first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{name} already registered"
                )
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        hashed_id = UserService._hash_pii(user_data.email)
        logger.info(f"Creating user with identifier: {hashed_id}")
        
        if user_data.idempotency_key:
            existing = db.query(User).filter(
                User.version == user_data.idempotency_key,
                User.is_deleted == False
            ).first()
            if existing:
                logger.info(f"Duplicate request detected via idempotency key, returning existing user: {existing.id}")
                return existing
        
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email and existing_email.is_deleted:
            logger.info(f"Restoring soft-deleted user with identifier: {hashed_id}")
            UserService._check_unique_fields(db, user_data, exclude_id=existing_email.id)
            for field, value in user_data.model_dump().items():
                setattr(existing_email, field, value)
            existing_email.is_deleted = False
            existing_email.deleted_at = None
            existing_email.deleted_by = None
            existing_email.is_active = True
            existing_email.version = str(uuid.uuid4())
            db.commit()
            db.refresh(existing_email)
            logger.info(f"User restored successfully: {existing_email.id}")
            return existing_email
        
        UserService._check_unique_fields(db, user_data)
        
        try:
            
            user_dict = user_data.model_dump(exclude={'idempotency_key'})
            db_user = User(**user_dict)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"User created successfully: {db_user.id}")
            return db_user
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Failed to create user with identifier {hashed_id}: {str(e)}")
            error_msg = str(e.orig)
            if 'email' in error_msg:
                detail = "Email already exists"
            elif 'primary_mobile' in error_msg:
                detail = "Mobile number already exists"
            elif 'aadhaar' in error_msg:
                detail = "Aadhaar already exists"
            elif 'pan' in error_msg:
                detail = "PAN already exists"
            else:
                detail = "Duplicate entry found"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        logger.debug(f"Fetching user: {user_id}")
        user = db.query(User).filter(and_(User.id == user_id, User.is_deleted == False)).first()
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: str, user_data: UserUpdate) -> User:
        logger.info(f"Updating user: {user_id}")
        db_user = UserService.get_user_by_id(db, user_id)
        update_data = user_data.model_dump(exclude_unset=True)
        
        if not update_data:
            logger.debug(f"No updates provided for user: {user_id}")
            return db_user
        
        temp_user = UserCreate(
            name=update_data.get('name', db_user.name),
            email=update_data.get('email', db_user.email),
            primary_mobile=update_data.get('primary_mobile', db_user.primary_mobile),
            secondary_mobile=update_data.get('secondary_mobile', db_user.secondary_mobile),
            aadhaar=db_user.aadhaar,
            pan=db_user.pan,
            date_of_birth=db_user.date_of_birth,
            place_of_birth=db_user.place_of_birth,
            current_address=update_data.get('current_address', db_user.current_address),
            permanent_address=update_data.get('permanent_address', db_user.permanent_address)
        )
        UserService._check_unique_fields(db, temp_user, exclude_id=user_id)
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db_user.version = str(uuid.uuid4())
        db.commit()
        db.refresh(db_user)
        logger.info(f"User updated successfully: {user_id}")
        return db_user
    
    @staticmethod
    def get_all_users(db: Session, page: int = 1, page_size: int = 10):
        logger.debug(f"Fetching users - page: {page}, page_size: {page_size}")
        offset = (page - 1) * page_size
        total = db.query(User).filter(User.is_deleted == False).count()
        users = db.query(User).filter(User.is_deleted == False)\
            .order_by(User.created_at.desc())\
            .offset(offset)\
            .limit(page_size)\
            .all()
        total_pages = (total + page_size - 1) // page_size
        logger.info(f"Fetched {len(users)} users (total: {total})")
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "data": users
        }
    
    @staticmethod
    def soft_delete_user(db: Session, user_id: str) -> User:
        logger.info(f"Soft deleting user: {user_id}")
        db_user = UserService.get_user_by_id(db, user_id)
        db_user.is_deleted = True
        db_user.deleted_at = datetime.utcnow()
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
        logger.info(f"User soft deleted successfully: {user_id}")
        return db_user
    
    @staticmethod
    def search_users(db: Session, query: str, page: int = 1, page_size: int = 10):
        logger.debug(f"Searching users with query: {query}")
        search_pattern = f"%{query}%"
        base_query = db.query(User).filter(
            User.is_deleted == False,
            (User.name.like(search_pattern) | User.email.like(search_pattern))
        )
        
        offset = (page - 1) * page_size
        total = base_query.count()
        users = base_query.order_by(User.created_at.desc())\
            .offset(offset)\
            .limit(page_size)\
            .all()
        
        total_pages = (total + page_size - 1) // page_size
        logger.info(f"Search found {total} users matching query")
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "data": users
        }