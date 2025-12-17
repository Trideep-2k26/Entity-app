from sqlalchemy import Column, String, DateTime, Boolean, Date, Text, Index
from sqlalchemy.sql import func
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    primary_mobile = Column(String(15), nullable=False, unique=True, index=True)
    secondary_mobile = Column(String(15), nullable=True)
    aadhaar = Column(String(12), nullable=False, unique=True, index=True)
    pan = Column(String(10), nullable=False, unique=True, index=True)
    date_of_birth = Column(Date, nullable=False)
    place_of_birth = Column(String(255), nullable=False)
    current_address = Column(Text, nullable=False)
    permanent_address = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(String(36), nullable=True)
    version = Column(String(36), default=lambda: str(uuid.uuid4()), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    mobile_verified = Column(Boolean, default=False, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        Index('idx_active_email', 'is_deleted', 'email'),
        Index('idx_active_mobile', 'is_deleted', 'primary_mobile'),
        Index('idx_active_aadhaar', 'is_deleted', 'aadhaar'),
        Index('idx_active_pan', 'is_deleted', 'pan'),
        Index('idx_name_search', 'name'),
        Index('idx_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"