# Complete User Management System Guide

## Part 1: View Database Tables in MySQL

### Method A: MySQL Command Line
```sql
-- Connect to MySQL
mysql -u root -p
-- Enter password: Trideep@2003

-- Select the database
USE user_management;

-- Show all tables
SHOW TABLES;

-- View table structure
DESCRIBE users;

-- View all data in users table
SELECT * FROM users;

-- Count total users
SELECT COUNT(*) FROM users;

-- Exit MySQL
EXIT;
```

### Method B: MySQL Workbench (GUI)
1. Open MySQL Workbench
2. Connect to your local MySQL instance
3. Double-click `user_management` database in the left panel
4. Click on "Tables" to see all tables
5. Right-click on `users` table → "Select Rows - Limit 1000"

---

## Part 2: Using Swagger UI (/docs) - EASIEST METHOD

### Step 1: Open Swagger UI
Open your browser and go to: **http://localhost:8000/docs**

### Step 2: Create a User

1. Find **POST /api/v1/users/** endpoint
2. Click on it to expand
3. Click **"Try it out"** button
4. You'll see a JSON template - edit it:

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

5. Click **"Execute"** button
6. See the response below with the created user (including ID)

### Step 3: Get All Users

1. Find **GET /api/v1/users/** endpoint
2. Click to expand
3. Click **"Try it out"**
4. (Optional) Set pagination parameters:
   - `page`: 1
   - `page_size`: 10
5. Click **"Execute"**
6. See all users in the response

### Step 4: Get Single User by ID

1. Find **GET /api/v1/users/{user_id}** endpoint
2. Click to expand
3. Click **"Try it out"**
4. Enter user ID (e.g., `1`)
5. Click **"Execute"**
6. See that specific user's details

### Step 5: Update User

1. Find **PUT /api/v1/users/{user_id}** endpoint
2. Click to expand
3. Click **"Try it out"**
4. Enter user ID
5. Edit the JSON with updated data
6. Click **"Execute"**

### Step 6: Search Users

1. Find **GET /api/v1/users/search/** endpoint
2. Click to expand
3. Click **"Try it out"**
4. Fill in search parameters (name, email, mobile, etc.)
5. Click **"Execute"**

### Step 7: Delete User (Soft Delete)

1. Find **DELETE /api/v1/users/{user_id}** endpoint
2. Click to expand
3. Click **"Try it out"**
4. Enter user ID
5. Click **"Execute"**

---

## Part 3: Using PowerShell with curl / Invoke-RestMethod

### Create User

**Using Invoke-RestMethod (Recommended for PowerShell):**
```powershell
$body = @{
    name = "Priya Sharma"
    email = "priya.sharma@example.com"
    primary_mobile = "9876543210"
    secondary_mobile = "8765432109"
    aadhaar = "987654321012"
    pan = "FGHIJ5678K"
    date_of_birth = "1995-05-20"
    place_of_birth = "Delhi"
    current_address = "45 Connaught Place, New Delhi"
    permanent_address = "78 Defence Colony, Delhi"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# Display the response
$response

# Save the user ID for later use
$userId = $response.id
Write-Host "Created user with ID: $userId" -ForegroundColor Green
```

**Using curl.exe:**
```powershell
curl.exe -X POST "http://localhost:8000/api/v1/users/" `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Amit Singh\",\"email\":\"amit@example.com\",\"primary_mobile\":\"9876543210\",\"secondary_mobile\":\"8765432109\",\"aadhaar\":\"111222333444\",\"pan\":\"KLMNO1234P\",\"date_of_birth\":\"1992-03-10\",\"place_of_birth\":\"Bangalore\",\"current_address\":\"12 MG Road, Bangalore\",\"permanent_address\":\"34 Brigade Road, Bangalore\"}'
```

### Get All Users

```powershell
# Get all users (page 1, 10 items)
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/" -Method GET

# Pretty print
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/" | ConvertTo-Json -Depth 5

# With pagination
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/?page=1&page_size=5"
```

### Get User by ID

```powershell
# Get user with ID 1
$user = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/1" -Method GET
$user

# Display specific fields
Write-Host "Name: $($user.name)"
Write-Host "Email: $($user.email)"
Write-Host "Mobile: $($user.primary_mobile)"
```

### Update User

```powershell
$updateBody = @{
    name = "Priya Sharma Updated"
    email = "priya.updated@example.com"
    primary_mobile = "9876543210"
    secondary_mobile = "8765432109"
    aadhaar = "987654321012"
    pan = "FGHIJ5678K"
    date_of_birth = "1995-05-20"
    place_of_birth = "Delhi"
    current_address = "New Address, Delhi"
    permanent_address = "New Permanent Address, Delhi"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/1" `
    -Method PUT `
    -Headers @{"Content-Type"="application/json"} `
    -Body $updateBody
```

### Search Users

```powershell
# Search by name
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?name=Priya"

# Search by email
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?email=example.com"

# Search by mobile
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?mobile=9876543210"

# Search by Aadhaar
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?aadhaar=123456789012"

# Search by PAN
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/search/?pan=ABCDE1234F"
```

### Delete User (Soft Delete)

```powershell
# Delete user with ID 1
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/users/1" -Method DELETE
```

---

## Part 4: Using Postman

### Setup Postman

1. Download Postman from https://www.postman.com/downloads/
2. Install and open it
3. Create a new Collection called "User Management API"

### Create Requests

#### 1. Create User (POST)
- **Method:** POST
- **URL:** `http://localhost:8000/api/v1/users/`
- **Headers:** 
  - Key: `Content-Type`, Value: `application/json`
- **Body:** (Select "raw" and "JSON")
```json
{
  "name": "Test User",
  "email": "test@example.com",
  "primary_mobile": "9876543210",
  "secondary_mobile": "8765432109",
  "aadhaar": "123456789012",
  "pan": "ABCDE1234F",
  "date_of_birth": "1990-01-15",
  "place_of_birth": "Mumbai",
  "current_address": "123 Test Street",
  "permanent_address": "456 Test Avenue"
}
```
- Click **Send**

#### 2. Get All Users (GET)
- **Method:** GET
- **URL:** `http://localhost:8000/api/v1/users/`
- **Params:** (optional)
  - `page`: 1
  - `page_size`: 10
- Click **Send**

#### 3. Get User by ID (GET)
- **Method:** GET
- **URL:** `http://localhost:8000/api/v1/users/1`
- Click **Send**

#### 4. Update User (PUT)
- **Method:** PUT
- **URL:** `http://localhost:8000/api/v1/users/1`
- **Headers:** `Content-Type: application/json`
- **Body:** (Updated JSON)
- Click **Send**

#### 5. Search Users (GET)
- **Method:** GET
- **URL:** `http://localhost:8000/api/v1/users/search/`
- **Params:**
  - `name`: Rajesh
  - `email`: example.com
- Click **Send**

#### 6. Delete User (DELETE)
- **Method:** DELETE
- **URL:** `http://localhost:8000/api/v1/users/1`
- Click **Send**

---

## Part 5: Complete Test Workflow

### Complete PowerShell Test Script

Save as `test-full-workflow.ps1`:

```powershell
# Complete API Test Workflow
$baseUrl = "http://localhost:8000"

Write-Host "`n=== User Management System - Complete Test ===" -ForegroundColor Cyan

# 1. Health Check
Write-Host "`n[1] Health Check..." -ForegroundColor Yellow
$health = Invoke-RestMethod -Uri "$baseUrl/health"
Write-Host "Status: $($health.status)" -ForegroundColor Green

# 2. Create First User
Write-Host "`n[2] Creating first user..." -ForegroundColor Yellow
$user1 = @{
    name = "Rajesh Kumar"
    email = "rajesh@example.com"
    primary_mobile = "9876543210"
    secondary_mobile = "8765432109"
    aadhaar = "123456789012"
    pan = "ABCDE1234F"
    date_of_birth = "1990-01-15"
    place_of_birth = "Mumbai"
    current_address = "123 MG Road, Mumbai"
    permanent_address = "456 Station Road, Pune"
} | ConvertTo-Json

$createdUser1 = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $user1

Write-Host "✓ Created user: $($createdUser1.name) (ID: $($createdUser1.id))" -ForegroundColor Green

# 3. Create Second User
Write-Host "`n[3] Creating second user..." -ForegroundColor Yellow
$user2 = @{
    name = "Priya Sharma"
    email = "priya@example.com"
    primary_mobile = "8765432109"
    secondary_mobile = "7654321098"
    aadhaar = "987654321012"
    pan = "FGHIJ5678K"
    date_of_birth = "1995-05-20"
    place_of_birth = "Delhi"
    current_address = "45 CP, New Delhi"
    permanent_address = "78 Defence Colony, Delhi"
} | ConvertTo-Json

$createdUser2 = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $user2

Write-Host "✓ Created user: $($createdUser2.name) (ID: $($createdUser2.id))" -ForegroundColor Green

# 4. Get All Users
Write-Host "`n[4] Getting all users..." -ForegroundColor Yellow
$allUsers = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/"
Write-Host "✓ Total users: $($allUsers.total)" -ForegroundColor Green
Write-Host "Users on this page:" -ForegroundColor Cyan
foreach ($user in $allUsers.items) {
    Write-Host "  - ID: $($user.id), Name: $($user.name), Email: $($user.email)"
}

# 5. Get User by ID
Write-Host "`n[5] Getting user by ID..." -ForegroundColor Yellow
$singleUser = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/$($createdUser1.id)"
Write-Host "✓ User: $($singleUser.name)" -ForegroundColor Green
Write-Host "  Email: $($singleUser.email)"
Write-Host "  Mobile: $($singleUser.primary_mobile)"

# 6. Update User
Write-Host "`n[6] Updating user..." -ForegroundColor Yellow
$updateData = @{
    name = "Rajesh Kumar Updated"
    email = "rajesh.updated@example.com"
    primary_mobile = "9999999999"
    secondary_mobile = "8888888888"
    aadhaar = "123456789012"
    pan = "ABCDE1234F"
    date_of_birth = "1990-01-15"
    place_of_birth = "Mumbai"
    current_address = "Updated Address, Mumbai"
    permanent_address = "Updated Permanent, Pune"
} | ConvertTo-Json

$updatedUser = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/$($createdUser1.id)" `
    -Method PUT `
    -Headers @{"Content-Type"="application/json"} `
    -Body $updateData

Write-Host "✓ Updated user: $($updatedUser.name)" -ForegroundColor Green

# 7. Search Users
Write-Host "`n[7] Searching users by name..." -ForegroundColor Yellow
$searchResult = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/search/?name=Priya"
Write-Host "✓ Found $($searchResult.total) user(s)" -ForegroundColor Green
foreach ($user in $searchResult.items) {
    Write-Host "  - $($user.name)"
}

# 8. Search by Email
Write-Host "`n[8] Searching users by email domain..." -ForegroundColor Yellow
$emailSearch = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/search/?email=example.com"
Write-Host "✓ Found $($emailSearch.total) user(s) with 'example.com'" -ForegroundColor Green

# 9. Delete User (Soft Delete)
Write-Host "`n[9] Deleting user..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "$baseUrl/api/v1/users/$($createdUser1.id)" -Method DELETE
Write-Host "✓ User deleted (soft delete)" -ForegroundColor Green

# 10. Verify Deletion
Write-Host "`n[10] Verifying deletion..." -ForegroundColor Yellow
try {
    $deletedUser = Invoke-RestMethod -Uri "$baseUrl/api/v1/users/$($createdUser1.id)"
    Write-Host "✓ User still accessible (deleted_at: $($deletedUser.deleted_at))" -ForegroundColor Yellow
} catch {
    Write-Host "✓ User not found (fully deleted)" -ForegroundColor Green
}

Write-Host "`n=== All Tests Completed Successfully! ===" -ForegroundColor Cyan
Write-Host "`nView API docs at: http://localhost:8000/docs" -ForegroundColor Magenta
```

Run it:
```powershell
.\test-full-workflow.ps1
```

---

## Summary of All Methods

| Task | Swagger UI | PowerShell | Postman | MySQL |
|------|-----------|------------|---------|-------|
| **Create User** | ✓ Easiest | ✓ Scriptable | ✓ GUI | ✗ |
| **View Users** | ✓ Visual | ✓ Command | ✓ GUI | ✓ Direct DB |
| **Update User** | ✓ Easy | ✓ Scriptable | ✓ GUI | ✓ Raw SQL |
| **Delete User** | ✓ Easy | ✓ Scriptable | ✓ GUI | ✓ Raw SQL |
| **Search** | ✓ Easy | ✓ Scriptable | ✓ GUI | ✓ SQL WHERE |

### Recommended for Beginners:
1. **Swagger UI** (http://localhost:8000/docs) - Visual, interactive, easiest!
2. **Postman** - Professional API testing tool
3. **PowerShell** - Automation and scripting
4. **MySQL CLI** - Direct database access

Try Swagger UI first - it's the easiest! 🚀
