# API Testing Guide for PowerShell

## Prerequisites
- Server running on http://localhost:8000
- PowerShell terminal

## PowerShell curl Commands

### 1. Create a User (POST)

```powershell
curl.exe -X POST "http://localhost:8000/api/v1/users/" `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Rajesh Kumar\",\"email\":\"rajesh.kumar@example.com\",\"primary_mobile\":\"9876543210\",\"secondary_mobile\":\"8765432109\",\"aadhaar\":\"123456789012\",\"pan\":\"ABCDE1234F\",\"date_of_birth\":\"1990-01-15\",\"place_of_birth\":\"Mumbai\",\"current_address\":\"123 MG Road, Andheri West, Mumbai, Maharashtra 400058\",\"permanent_address\":\"456 Station Road, Pune, Maharashtra 411001\"}'
```

**Alternative (more readable with JSON file):**
```powershell
# Save this as user.json first
@"
{
  "name": "Rajesh Kumar",
  "email": "rajesh.kumar@example.com",
  "primary_mobile": "9876543210",
  "secondary_mobile": "8765432109",
  "aadhaar": "123456789012",
  "pan": "ABCDE1234F",
  "date_of_birth": "1990-01-15",
  "place_of_birth": "Mumbai",
  "current_address": "123 MG Road, Andheri West, Mumbai, Maharashtra 400058",
  "permanent_address": "456 Station Road, Pune, Maharashtra 411001"
}
"@ | Out-File -FilePath user.json -Encoding utf8

# Then POST it
curl.exe -X POST "http://localhost:8000/api/v1/users/" `
  -H "Content-Type: application/json" `
  -d "@user.json"
```

**Using Invoke-RestMethod (Recommended for PowerShell):**
```powershell
$body = @{
    name = "Rajesh Kumar"
    email = "rajesh.kumar@example.com"
    primary_mobile = "9876543210"
    secondary_mobile = "8765432109"
    aadhaar = "123456789012"
    pan = "ABCDE1234F"
    date_of_birth = "1990-01-15"
    place_of_birth = "Mumbai"
    current_address = "123 MG Road, Andheri West, Mumbai, Maharashtra 400058"
    permanent_address = "456 Station Road, Pune, Maharashtra 411001"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

### 2. Get All Users (GET)

```powershell
# Simple GET
curl.exe http://localhost:8000/api/v1/users/

# Or using Invoke-RestMethod (better formatting)
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/" -Method GET
```

**With pagination:**
```powershell
# Page 1, 10 items
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/?page=1&page_size=10" -Method GET

# Page 2, 5 items
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/?page=2&page_size=5" -Method GET
```

### 3. Get User by ID (GET)

```powershell
# Get user with ID 1
curl.exe http://localhost:8000/api/v1/users/1

# Or
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/1" -Method GET
```

### 4. Update User (PUT)

```powershell
$updateBody = @{
    name = "Rajesh Kumar Updated"
    email = "rajesh.updated@example.com"
    primary_mobile = "9876543210"
    secondary_mobile = "8765432109"
    aadhaar = "123456789012"
    pan = "ABCDE1234F"
    date_of_birth = "1990-01-15"
    place_of_birth = "Mumbai"
    current_address = "Updated Address"
    permanent_address = "Updated Permanent Address"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/1" `
  -Method PUT `
  -Headers @{"Content-Type"="application/json"} `
  -Body $updateBody
```

### 5. Delete User (DELETE)

```powershell
# Soft delete user with ID 1
curl.exe -X DELETE http://localhost:8000/api/v1/users/1

# Or
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/1" -Method DELETE
```

### 6. Search Users (GET)

```powershell
# Search by name
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?name=Rajesh" -Method GET

# Search by email
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?email=rajesh" -Method GET

# Search by mobile
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?mobile=9876543210" -Method GET

# Search by Aadhaar
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?aadhaar=123456789012" -Method GET

# Search by PAN
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?pan=ABCDE1234F" -Method GET

# Multiple filters
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?name=Rajesh&email=example.com" -Method GET
```

### 7. Health Check

```powershell
curl.exe http://localhost:8000/health

# Or
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
```

## Complete Test Script

Save this as `test-api.ps1`:

```powershell
# Test API Script
$baseUrl = "http://localhost:8000"

Write-Host "=== Testing User Management API ===" -ForegroundColor Green

# 1. Health Check
Write-Host "`n1. Health Check..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$baseUrl/health" -Method GET

# 2. Create User
Write-Host "`n2. Creating new user..." -ForegroundColor Yellow
$newUser = @{
    name = "Test User $(Get-Random)"
    email = "test$(Get-Random)@example.com"
    primary_mobile = "9876543210"
    secondary_mobile = "8765432109"
    aadhaar = "123456789012"
    pan = "ABCDE1234F"
    date_of_birth = "1990-01-15"
    place_of_birth = "Mumbai"
    current_address = "123 Test Street"
    permanent_address = "456 Test Avenue"
} | ConvertTo-Json

$createdUser = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $newUser

Write-Host "Created user with ID: $($createdUser.id)" -ForegroundColor Green
$userId = $createdUser.id

# 3. Get All Users
Write-Host "`n3. Getting all users..." -ForegroundColor Yellow
$allUsers = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/" -Method GET
Write-Host "Total users: $($allUsers.total)" -ForegroundColor Green

# 4. Get User by ID
Write-Host "`n4. Getting user by ID: $userId..." -ForegroundColor Yellow
$user = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/$userId" -Method GET
Write-Host "User name: $($user.name)" -ForegroundColor Green

# 5. Update User
Write-Host "`n5. Updating user..." -ForegroundColor Yellow
$updateData = @{
    name = "Updated Test User"
    email = $createdUser.email
    primary_mobile = "9876543210"
    secondary_mobile = "8765432109"
    aadhaar = "123456789012"
    pan = "ABCDE1234F"
    date_of_birth = "1990-01-15"
    place_of_birth = "Mumbai"
    current_address = "Updated Address"
    permanent_address = "Updated Permanent"
} | ConvertTo-Json

$updatedUser = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/$userId" `
  -Method PUT `
  -Headers @{"Content-Type"="application/json"} `
  -Body $updateData

Write-Host "Updated user name: $($updatedUser.name)" -ForegroundColor Green

# 6. Search Users
Write-Host "`n6. Searching users..." -ForegroundColor Yellow
$searchResult = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/search/?name=Updated" -Method GET
Write-Host "Found users: $($searchResult.total)" -ForegroundColor Green

# 7. Delete User
Write-Host "`n7. Deleting user..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$baseUrl/api/v1/users/$userId" -Method DELETE
Write-Host "User deleted successfully" -ForegroundColor Green

Write-Host "`n=== All Tests Completed ===" -ForegroundColor Green
```

Run it with:
```powershell
.\test-api.ps1
```

## Tips for PowerShell

1. **Use `curl.exe`** (not just `curl`) to use the real curl, not the PowerShell alias
2. **Use `Invoke-RestMethod`** for better JSON handling in PowerShell
3. **Escape quotes** in JSON strings with backslash when using curl.exe
4. **Use backticks** (`) for line continuation in PowerShell
5. **Pretty print JSON**:
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/" | ConvertTo-Json -Depth 10
   ```

## Browser Testing (Easiest)

Just open these URLs in your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Click "Try it out" on any endpoint to test it interactively!
