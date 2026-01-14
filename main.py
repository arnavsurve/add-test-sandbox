#!/usr/bin/env python3
"""
Basic FastAPI web server for Personal Photo Blog
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Personal Photo Blog API",
    description="A REST API for managing a personal photo blog",
    version="1.0.0"
)

# In-memory storage for photos
photos_db = []
photo_id_counter = 1


class Photo(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    tags: Optional[List[str]] = []


class PhotoResponse(Photo):
    id: int
    created_at: str


@app.get("/")
def read_root():
    """Root endpoint - returns API information"""
    return {
        "message": "Welcome to Personal Photo Blog API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "GET /photos": "List all photos",
            "GET /photos/{photo_id}": "Get a specific photo",
            "POST /photos": "Create a new photo",
            "PUT /photos/{photo_id}": "Update a photo",
            "DELETE /photos/{photo_id}": "Delete a photo"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "photos_count": len(photos_db)
    }


@app.get("/photos", response_model=List[PhotoResponse])
def list_photos(tag: Optional[str] = None):
    """List all photos, optionally filtered by tag"""
    if tag:
        filtered_photos = [p for p in photos_db if tag in p.get("tags", [])]
        return filtered_photos
    return photos_db


@app.get("/photos/{photo_id}", response_model=PhotoResponse)
def get_photo(photo_id: int):
    """Get a specific photo by ID"""
    for photo in photos_db:
        if photo["id"] == photo_id:
            return photo
    raise HTTPException(status_code=404, detail=f"Photo with id {photo_id} not found")


@app.post("/photos", response_model=PhotoResponse, status_code=201)
def create_photo(photo: Photo):
    """Create a new photo entry"""
    global photo_id_counter
    
    new_photo = {
        "id": photo_id_counter,
        "title": photo.title,
        "description": photo.description,
        "url": photo.url,
        "tags": photo.tags or [],
        "created_at": datetime.utcnow().isoformat()
    }
    
    photos_db.append(new_photo)
    photo_id_counter += 1
    
    return new_photo


@app.put("/photos/{photo_id}", response_model=PhotoResponse)
def update_photo(photo_id: int, photo: Photo):
    """Update an existing photo"""
    for i, existing_photo in enumerate(photos_db):
        if existing_photo["id"] == photo_id:
            updated_photo = {
                "id": photo_id,
                "title": photo.title,
                "description": photo.description,
                "url": photo.url,
                "tags": photo.tags or [],
                "created_at": existing_photo["created_at"]
            }
            photos_db[i] = updated_photo
            return updated_photo
    
    raise HTTPException(status_code=404, detail=f"Photo with id {photo_id} not found")


@app.delete("/photos/{photo_id}")
def delete_photo(photo_id: int):
    """Delete a photo"""
    for i, photo in enumerate(photos_db):
        if photo["id"] == photo_id:
            deleted_photo = photos_db.pop(i)
            return {
                "message": f"Photo {photo_id} deleted successfully",
                "deleted_photo": deleted_photo
            }
    
    raise HTTPException(status_code=404, detail=f"Photo with id {photo_id} not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
