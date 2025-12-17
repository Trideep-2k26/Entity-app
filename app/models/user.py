from sqlalchemy import Column, String, DateTime, Boolean, Date, Text
from sqlalchemy.sql import func
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    # Primary Key - Using UUID for better security and distribution
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Personal Information
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    primary_mobile = Column(String(15), nullable=False, unique=True, index=True)
    secondary_mobile = Column(String(15), nullable=True)
    
    # Government IDs - Encrypted in production
    aadhaar = Column(String(12), nullable=False, unique=True, index=True)
    pan = Column(String(10), nullable=False, unique=True, index=True)
    
    # Birth Information
    date_of_birth = Column(Date, nullable=False)
    place_of_birth = Column(String(255), nullable=False)
    
    # Address Information
    current_address = Column(Text, nullable=False)
    permanent_address = Column(Text, nullable=False)
    
    # Audit Fields - Best Practice for tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    created_by = Column(String(36), nullable=True)  # User ID who created
    updated_by = Column(String(36), nullable=True)  # User ID who last updated
    
    # Soft Delete - Best Practice instead of hard delete
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(String(36), nullable=True)
    
    # Versioning - For audit trail
    version = Column(String(36), default=lambda: str(uuid.uuid4()), nullable=False)
    
    # Additional useful fields
    is_active = Column(Boolean, default=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    mobile_verified = Column(Boolean, default=False, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"