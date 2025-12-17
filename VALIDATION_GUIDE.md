# Quick Test - Valid User Data Examples

## Your Current Data (Should Work):
```json
{
  "name": "Rajesh Kumar",
  "email": "rajesh@example.com",
  "primary_mobile": "9876543210",
  "secondary_mobile": "8765432109",
  "aadhaar": "123456789012",
  "pan": "ABCDE1234F",
  "date_of_birth": "1990-01-15",
  "place_of_birth": "Mumbai",
  "current_address": "123 MG Road, Mumbai",
  "permanent_address": "456 Station Road, Pune"
}
```

This data is VALID! ✓

## Why You're Getting 422 Error:

**Possible reasons:**

### 1. Email Already Exists (Most Likely)
If you already created a user with `rajesh@example.com`, you can't create another with the same email.

**Solution:** Change the email:
```json
{
  "name": "Priya Sharma",
  "email": "priya@example.com",
  "primary_mobile": "8765432109",
  "secondary_mobile": "7654321098",
  "aadhaar": "987654321012",
  "pan": "FGHIJ5678K",
  "date_of_birth": "1995-05-20",
  "place_of_birth": "Delhi",
  "current_address": "45 Connaught Place, New Delhi",
  "permanent_address": "78 Defence Colony, Delhi"
}
```

### 2. Unique Constraints
These fields must be unique (no duplicates):
- ✓ Email
- ✓ Primary Mobile
- ✓ Aadhaar
- ✓ PAN

### 3. Validation Rules

**Mobile Numbers:**
- Must start with 6, 7, 8, or 9
- Must be exactly 10 digits
- ✓ Valid: `9876543210`
- ✗ Invalid: `1234567890`, `987654321`

**Aadhaar:**
- Must be exactly 12 digits
- ✓ Valid: `123456789012`
- ✗ Invalid: `12345678901`, `ABCD12345678`

**PAN:**
- Format: 5 letters + 4 digits + 1 letter (uppercase)
- ✓ Valid: `ABCDE1234F`
- ✗ Invalid: `ABCD1234F`, `abcde1234f`, `12345ABCDE`

**Age:**
- Must be at least 18 years old
- ✓ Valid: `1990-01-15` (35 years old)
- ✗ Invalid: `2010-01-15` (15 years old)

**Address:**
- Minimum 10 characters
- Maximum 1000 characters

## How to See the Exact Error in Swagger:

1. Go to http://localhost:8000/docs
2. Try to create user
3. Click "Execute"
4. Scroll down to **Response body** - it will show the exact error!

Example error response:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Email already registered",
      "type": "value_error"
    }
  ]
}
```

## Test Data - Copy & Paste Ready:

### User 1:
```json
{
  "name": "Amit Singh",
  "email": "amit.singh@example.com",
  "primary_mobile": "9123456789",
  "secondary_mobile": "8123456789",
  "aadhaar": "111222333444",
  "pan": "KLMNO1234P",
  "date_of_birth": "1992-03-10",
  "place_of_birth": "Bangalore",
  "current_address": "12 MG Road, Bangalore, Karnataka 560001",
  "permanent_address": "34 Brigade Road, Bangalore, Karnataka 560001"
}
```

### User 2:
```json
{
  "name": "Sneha Patel",
  "email": "sneha.patel@example.com",
  "primary_mobile": "7234567890",
  "secondary_mobile": "6234567890",
  "aadhaar": "555666777888",
  "pan": "QRSTU5678V",
  "date_of_birth": "1988-07-25",
  "place_of_birth": "Ahmedabad",
  "current_address": "88 CG Road, Ahmedabad, Gujarat 380009",
  "permanent_address": "99 SG Highway, Ahmedabad, Gujarat 380015"
}
```

### User 3:
```json
{
  "name": "Vikram Reddy",
  "email": "vikram.reddy@example.com",
  "primary_mobile": "8345678901",
  "secondary_mobile": "9345678901",
  "aadhaar": "999888777666",
  "pan": "WXYZH9012A",
  "date_of_birth": "1985-11-30",
  "place_of_birth": "Hyderabad",
  "current_address": "77 Banjara Hills, Hyderabad, Telangana 500034",
  "permanent_address": "55 Jubilee Hills, Hyderabad, Telangana 500033"
}
```

## PowerShell Command to Check Existing Users:

```powershell
# See what users already exist
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/" | 
    Select-Object -ExpandProperty items | 
    Select-Object id, name, email, primary_mobile, aadhaar, pan
```

## Quick Fix:

If user creation is failing, check existing users and use DIFFERENT:
- Email
- Mobile number
- Aadhaar
- PAN

Each must be unique! 🎯
