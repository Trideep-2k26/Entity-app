import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "mysql+pymysql://test:test@localhost:3306/test_user_management"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user_data():
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "primary_mobile": "9876543210",
        "secondary_mobile": "8765432109",
        "aadhaar": "123456789012",
        "pan": "ABCDE1234F",
        "date_of_birth": "1990-01-01",
        "place_of_birth": "Mumbai",
        "current_address": "123 Main St, Mumbai, Maharashtra, India",
        "permanent_address": "456 Oak St, Mumbai, Maharashtra, India"
    }
