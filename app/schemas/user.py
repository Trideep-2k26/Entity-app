from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime
from typing import Optional
from app.utils.validators import Validators

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    primary_mobile: str = Field(..., pattern=r'^[6-9]\d{9}$', description="Primary mobile")
    secondary_mobile: Optional[str] = Field(None, pattern=r'^[6-9]\d{9}$', description="Secondary mobile")
    aadhaar: str = Field(..., min_length=12, max_length=12, description="Aadhaar number")
    pan: str = Field(..., min_length=10, max_length=10, description="PAN number")
    date_of_birth: date = Field(..., description="Date of birth")
    place_of_birth: str = Field(..., min_length=2, max_length=255, description="Place of birth")
    current_address: str = Field(..., min_length=10, max_length=1000, description="Current address")
    permanent_address: str = Field(..., min_length=10, max_length=1000, description="Permanent address")
    
    @field_validator('aadhaar')
    @classmethod
    def validate_aadhaar(cls, v):
        if not Validators.validate_aadhaar(v):
            raise ValueError('Invalid Aadhaar number')
        return v
    
    @field_validator('pan')
    @classmethod
    def validate_pan(cls, v):
        if not Validators.validate_pan(v):
            raise ValueError('Invalid PAN number format')
        return v.upper()
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_dob(cls, v):
        if not Validators.validate_age(v):
            raise ValueError('User must be at least 18 years old')
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v

class UserCreate(UserBase):
    """Schema for creating a user"""
    idempotency_key: Optional[str] = Field(None, description="Client-generated unique key to prevent duplicate submissions")

class UserUpdate(BaseModel):
    """Schema for updating a user - all fields optional"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    primary_mobile: Optional[str] = Field(None, pattern=r'^[6-9]\d{9}$')
    secondary_mobile: Optional[str] = Field(None, pattern=r'^[6-9]\d{9}$')
    current_address: Optional[str] = Field(None, min_length=10, max_length=1000)
    permanent_address: Optional[str] = Field(None, min_length=10, max_length=1000)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """Schema for user response"""
    id: str
    is_active: bool
    email_verified: bool
    mobile_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class PaginatedUserResponse(BaseModel):
    """Schema for paginated response"""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: list[UserResponse]
