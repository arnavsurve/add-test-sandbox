#!/usr/bin/env python3
"""
Comprehensive test script for FastAPI endpoints
"""

import httpx
import time
import sys


BASE_URL = "http://localhost:8000"


def print_test(test_name):
    """Print test header"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print('='*60)


def print_result(response, expected_status=200):
    """Print test result"""
    success = response.status_code == expected_status
    status_icon = "✓" if success else "✗"
    print(f"{status_icon} Status Code: {response.status_code} (Expected: {expected_status})")
    print(f"Response: {response.json()}")
    return success


def test_api():
    """Run comprehensive API tests"""
    client = httpx.Client(base_url=BASE_URL, timeout=10.0)
    all_tests_passed = True
    
    try:
        # Test 1: Root endpoint
        print_test("GET / - Root Endpoint")
        response = client.get("/")
        all_tests_passed &= print_result(response)
        
        # Test 2: Health check
        print_test("GET /health - Health Check")
        response = client.get("/health")
        all_tests_passed &= print_result(response)
        
        # Test 3: List photos (empty)
        print_test("GET /photos - List Photos (Empty)")
        response = client.get("/photos")
        all_tests_passed &= print_result(response)
        assert response.json() == [], "Expected empty list"
        print("✓ Verified empty list")
        
        # Test 4: Create first photo
        print_test("POST /photos - Create Photo #1")
        photo1_data = {
            "title": "Sunset at the Beach",
            "description": "Beautiful sunset with vibrant colors",
            "url": "https://example.com/sunset.jpg",
            "tags": ["sunset", "beach", "nature"]
        }
        response = client.post("/photos", json=photo1_data)
        all_tests_passed &= print_result(response, 201)
        photo1_id = response.json()["id"]
        print(f"✓ Created photo with ID: {photo1_id}")
        
        # Test 5: Create second photo
        print_test("POST /photos - Create Photo #2")
        photo2_data = {
            "title": "Mountain Landscape",
            "description": "Snow-capped mountains in winter",
            "url": "https://example.com/mountain.jpg",
            "tags": ["mountain", "winter", "landscape"]
        }
        response = client.post("/photos", json=photo2_data)
        all_tests_passed &= print_result(response, 201)
        photo2_id = response.json()["id"]
        print(f"✓ Created photo with ID: {photo2_id}")
        
        # Test 6: Create third photo
        print_test("POST /photos - Create Photo #3")
        photo3_data = {
            "title": "City at Night",
            "description": "Urban skyline with lights",
            "url": "https://example.com/city.jpg",
            "tags": ["city", "night", "urban"]
        }
        response = client.post("/photos", json=photo3_data)
        all_tests_passed &= print_result(response, 201)
        photo3_id = response.json()["id"]
        print(f"✓ Created photo with ID: {photo3_id}")
        
        # Test 7: List all photos
        print_test("GET /photos - List All Photos")
        response = client.get("/photos")
        all_tests_passed &= print_result(response)
        photos = response.json()
        assert len(photos) == 3, f"Expected 3 photos, got {len(photos)}"
        print(f"✓ Verified 3 photos in database")
        
        # Test 8: Get specific photo
        print_test(f"GET /photos/{photo1_id} - Get Specific Photo")
        response = client.get(f"/photos/{photo1_id}")
        all_tests_passed &= print_result(response)
        photo = response.json()
        assert photo["title"] == "Sunset at the Beach", "Title mismatch"
        print("✓ Verified photo details")
        
        # Test 9: Filter photos by tag
        print_test("GET /photos?tag=nature - Filter by Tag")
        response = client.get("/photos", params={"tag": "nature"})
        all_tests_passed &= print_result(response)
        filtered = response.json()
        assert len(filtered) == 1, f"Expected 1 photo with 'nature' tag, got {len(filtered)}"
        print("✓ Verified tag filtering")
        
        # Test 10: Update photo
        print_test(f"PUT /photos/{photo2_id} - Update Photo")
        updated_data = {
            "title": "Mountain Landscape - Updated",
            "description": "Updated description with more details",
            "url": "https://example.com/mountain_hd.jpg",
            "tags": ["mountain", "winter", "landscape", "hd"]
        }
        response = client.put(f"/photos/{photo2_id}", json=updated_data)
        all_tests_passed &= print_result(response)
        updated_photo = response.json()
        assert updated_photo["title"] == "Mountain Landscape - Updated", "Update failed"
        assert "hd" in updated_photo["tags"], "Tag update failed"
        print("✓ Verified photo update")
        
        # Test 11: Get non-existent photo (should fail)
        print_test("GET /photos/9999 - Get Non-existent Photo (Error Test)")
        response = client.get("/photos/9999")
        all_tests_passed &= print_result(response, 404)
        
        # Test 12: Update non-existent photo (should fail)
        print_test("PUT /photos/9999 - Update Non-existent Photo (Error Test)")
        response = client.put("/photos/9999", json=photo1_data)
        all_tests_passed &= print_result(response, 404)
        
        # Test 13: Delete photo
        print_test(f"DELETE /photos/{photo3_id} - Delete Photo")
        response = client.delete(f"/photos/{photo3_id}")
        all_tests_passed &= print_result(response)
        
        # Test 14: Verify deletion
        print_test("GET /photos - Verify Photo Deleted")
        response = client.get("/photos")
        all_tests_passed &= print_result(response)
        photos = response.json()
        assert len(photos) == 2, f"Expected 2 photos after deletion, got {len(photos)}"
        print("✓ Verified photo deletion")
        
        # Test 15: Delete non-existent photo (should fail)
        print_test("DELETE /photos/9999 - Delete Non-existent Photo (Error Test)")
        response = client.delete("/photos/9999")
        all_tests_passed &= print_result(response, 404)
        
        # Test 16: Create photo with minimal data
        print_test("POST /photos - Create Photo with Minimal Data")
        minimal_photo = {
            "title": "Minimal Photo",
            "url": "https://example.com/minimal.jpg"
        }
        response = client.post("/photos", json=minimal_photo)
        all_tests_passed &= print_result(response, 201)
        photo = response.json()
        assert photo["description"] is None, "Expected None for description"
        assert photo["tags"] == [], "Expected empty list for tags"
        print("✓ Verified optional fields handling")
        
        # Final summary
        print("\n" + "="*60)
        if all_tests_passed:
            print("✓ ALL TESTS PASSED!")
        else:
            print("✗ SOME TESTS FAILED")
        print("="*60)
        
        return all_tests_passed
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        client.close()


def wait_for_server(max_retries=10, delay=1):
    """Wait for server to be ready"""
    print("Waiting for server to start...")
    for i in range(max_retries):
        try:
            response = httpx.get(f"{BASE_URL}/health", timeout=2.0)
            if response.status_code == 200:
                print(f"✓ Server is ready!")
                return True
        except (httpx.ConnectError, httpx.TimeoutException):
            print(f"  Attempt {i+1}/{max_retries}: Server not ready yet...")
            time.sleep(delay)
    
    print("✗ Server failed to start")
    return False


if __name__ == "__main__":
    if not wait_for_server():
        sys.exit(1)
    
    success = test_api()
    sys.exit(0 if success else 1)
