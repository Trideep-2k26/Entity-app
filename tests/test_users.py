import pytest
from fastapi import status

def test_create_user_success(client, sample_user_data):
    """Test successful user creation"""
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert data["name"] == sample_user_data["name"]
    assert "id" in data

def test_create_user_duplicate_email(client, sample_user_data):
    """Test duplicate email validation"""
    client.post("/api/v1/users/", json=sample_user_data)
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]

def test_create_user_invalid_email(client, sample_user_data):
    """Test invalid email validation"""
    sample_user_data["email"] = "invalid-email"
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_user_invalid_mobile(client, sample_user_data):
    """Test invalid mobile validation"""
    sample_user_data["primary_mobile"] = "1234567890"  # Invalid - doesn't start with 6-9
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_user_invalid_aadhaar(client, sample_user_data):
    """Test invalid Aadhaar validation"""
    sample_user_data["aadhaar"] = "12345"  # Too short
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_user_invalid_pan(client, sample_user_data):
    """Test invalid PAN validation"""
    sample_user_data["pan"] = "INVALID"
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_user_underage(client, sample_user_data):
    """Test age validation"""
    sample_user_data["date_of_birth"] = "2010-01-01"  # < 18 years
    response = client.post("/api/v1/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_user_success(client, sample_user_data):
    """Test get user by ID"""
    create_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == user_id

def test_get_user_not_found(client):
    """Test get non-existent user"""
    response = client.get("/api/v1/users/non-existent-id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_user_success(client, sample_user_data):
    """Test successful user update"""
    create_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]
    
    update_data = {"name": "Jane Doe", "current_address": "789 New St, Mumbai"}
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Jane Doe"
    assert response.json()["current_address"] == "789 New St, Mumbai"

def test_update_user_duplicate_email(client, sample_user_data):
    """Test update with duplicate email"""
    # Create first user
    client.post("/api/v1/users/", json=sample_user_data)
    
    # Create second user
    sample_user_data["email"] = "second@example.com"
    sample_user_data["primary_mobile"] = "9876543211"
    sample_user_data["aadhaar"] = "123456789013"
    sample_user_data["pan"] = "ABCDE1234G"
    create_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]
    
    # Try to update second user with first user's email
    response = client.put(f"/api/v1/users/{user_id}", json={"email": "john.doe@example.com"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_get_all_users_pagination(client, sample_user_data):
    """Test pagination in get all users"""
    # Create multiple users
    for i in range(15):
        user_data = sample_user_data.copy()
        user_data["email"] = f"user{i}@example.com"
        user_data["primary_mobile"] = f"987654{i:04d}"
        user_data["aadhaar"] = f"12345678{i:04d}"
        user_data["pan"] = f"ABCDE{1230+i:04d}F"  # Generate unique PANs: ABCDE1230F to ABCDE1244F
        client.post("/api/v1/users/", json=user_data)
    
    # Test first page
    response = client.get("/api/v1/users/?page=1&page_size=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total_pages"] == 2
    assert len(data["data"]) == 10
    
    # Test second page
    response = client.get("/api/v1/users/?page=2&page_size=10")
    data = response.json()
    assert len(data["data"]) == 5

def test_soft_delete_user(client, sample_user_data):
    """Test soft delete functionality"""
    create_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]
    
    # Delete user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Try to get deleted user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}

if __name__ == "__main__":
    pytest.main([__file__, "-v"])