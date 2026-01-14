#!/usr/bin/env python3
"""
Pytest-based tests for FastAPI application
Run with: pytest test_main.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app, photos_db, photo_id_counter


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test"""
    photos_db.clear()
    globals()["photo_id_counter"] = 1
    yield


client = TestClient(app)


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to Personal Photo Blog API"
    assert "version" in data
    assert "endpoints" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "photos_count" in data


def test_list_photos_empty():
    """Test listing photos when database is empty"""
    response = client.get("/photos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_photo():
    """Test creating a new photo"""
    photo_data = {
        "title": "Test Photo",
        "description": "A test photo",
        "url": "https://example.com/test.jpg",
        "tags": ["test", "photo"]
    }
    response = client.post("/photos", json=photo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Photo"
    assert data["description"] == "A test photo"
    assert data["url"] == "https://example.com/test.jpg"
    assert data["tags"] == ["test", "photo"]
    assert "id" in data
    assert "created_at" in data


def test_create_photo_minimal():
    """Test creating photo with minimal required fields"""
    photo_data = {
        "title": "Minimal Photo",
        "url": "https://example.com/minimal.jpg"
    }
    response = client.post("/photos", json=photo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minimal Photo"
    assert data["description"] is None
    assert data["tags"] == []


def test_get_photo():
    """Test getting a specific photo"""
    # Create a photo first
    photo_data = {
        "title": "Get Test",
        "url": "https://example.com/get.jpg"
    }
    create_response = client.post("/photos", json=photo_data)
    photo_id = create_response.json()["id"]
    
    # Get the photo
    response = client.get(f"/photos/{photo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == photo_id
    assert data["title"] == "Get Test"


def test_get_nonexistent_photo():
    """Test getting a photo that doesn't exist"""
    response = client.get("/photos/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_photos():
    """Test listing multiple photos"""
    # Create multiple photos
    for i in range(3):
        photo_data = {
            "title": f"Photo {i}",
            "url": f"https://example.com/photo{i}.jpg"
        }
        client.post("/photos", json=photo_data)
    
    # List all photos
    response = client.get("/photos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_filter_photos_by_tag():
    """Test filtering photos by tag"""
    # Create photos with different tags
    client.post("/photos", json={
        "title": "Nature Photo",
        "url": "https://example.com/nature.jpg",
        "tags": ["nature", "outdoor"]
    })
    client.post("/photos", json={
        "title": "City Photo",
        "url": "https://example.com/city.jpg",
        "tags": ["city", "urban"]
    })
    client.post("/photos", json={
        "title": "Nature Landscape",
        "url": "https://example.com/landscape.jpg",
        "tags": ["nature", "landscape"]
    })
    
    # Filter by 'nature' tag
    response = client.get("/photos", params={"tag": "nature"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Filter by 'city' tag
    response = client.get("/photos", params={"tag": "city"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_update_photo():
    """Test updating a photo"""
    # Create a photo
    photo_data = {
        "title": "Original Title",
        "url": "https://example.com/original.jpg",
        "tags": ["original"]
    }
    create_response = client.post("/photos", json=photo_data)
    photo_id = create_response.json()["id"]
    
    # Update the photo
    updated_data = {
        "title": "Updated Title",
        "description": "New description",
        "url": "https://example.com/updated.jpg",
        "tags": ["updated", "modified"]
    }
    response = client.put(f"/photos/{photo_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "New description"
    assert data["tags"] == ["updated", "modified"]
    assert data["id"] == photo_id


def test_update_nonexistent_photo():
    """Test updating a photo that doesn't exist"""
    photo_data = {
        "title": "Test",
        "url": "https://example.com/test.jpg"
    }
    response = client.put("/photos/9999", json=photo_data)
    assert response.status_code == 404


def test_delete_photo():
    """Test deleting a photo"""
    # Create a photo
    photo_data = {
        "title": "To Delete",
        "url": "https://example.com/delete.jpg"
    }
    create_response = client.post("/photos", json=photo_data)
    photo_id = create_response.json()["id"]
    
    # Delete the photo
    response = client.delete(f"/photos/{photo_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify it's deleted
    get_response = client.get(f"/photos/{photo_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_photo():
    """Test deleting a photo that doesn't exist"""
    response = client.delete("/photos/9999")
    assert response.status_code == 404


def test_photo_id_increment():
    """Test that photo IDs increment correctly"""
    ids = []
    for i in range(3):
        response = client.post("/photos", json={
            "title": f"Photo {i}",
            "url": f"https://example.com/photo{i}.jpg"
        })
        ids.append(response.json()["id"])
    
    assert ids == [1, 2, 3]


def test_photo_created_at_timestamp():
    """Test that created_at timestamp is present"""
    response = client.post("/photos", json={
        "title": "Timestamp Test",
        "url": "https://example.com/timestamp.jpg"
    })
    data = response.json()
    assert "created_at" in data
    assert "T" in data["created_at"]  # ISO format check


def test_update_preserves_created_at():
    """Test that updating a photo preserves the original created_at"""
    # Create a photo
    create_response = client.post("/photos", json={
        "title": "Original",
        "url": "https://example.com/original.jpg"
    })
    photo_id = create_response.json()["id"]
    original_created_at = create_response.json()["created_at"]
    
    # Update the photo
    update_response = client.put(f"/photos/{photo_id}", json={
        "title": "Updated",
        "url": "https://example.com/updated.jpg"
    })
    updated_created_at = update_response.json()["created_at"]
    
    assert original_created_at == updated_created_at
