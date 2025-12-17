import re
from datetime import date, datetime

class Validators:
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_mobile(mobile: str) -> bool:
        """Validate Indian mobile number (10 digits)"""
        pattern = r'^[6-9]\d{9}$'
        return bool(re.match(pattern, mobile))
    
    @staticmethod
    def validate_aadhaar(aadhaar: str) -> bool:
        """Validate Aadhaar number (12 digits)"""
        if not aadhaar.isdigit() or len(aadhaar) != 12:
            return False
        # Verhoeff algorithm check would go here in production
        return True
    
    @staticmethod
    def validate_pan(pan: str) -> bool:
        """Validate PAN number (ABCDE1234F format)"""
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        return bool(re.match(pattern, pan.upper()))
    
    @staticmethod
    def validate_age(dob: date, min_age: int = 18) -> bool:
        """Validate minimum age requirement"""
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age >= min_age
