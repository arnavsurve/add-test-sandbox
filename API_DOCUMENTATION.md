# FastAPI Photo Blog - API Documentation

## Overview

This is a RESTful API for managing a personal photo blog. It provides endpoints for creating, reading, updating, and deleting photo entries.

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Run directly with Python
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

### Running with Docker

```bash
# Build the Docker image
docker build -t photo-blog-api .

# Run the container
docker run -p 8000:8000 photo-blog-api
```

## Testing

### Run Automated Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run pytest tests (recommended - requires no running server)
pytest test_main.py -v

# Run manual integration tests (requires server to be running)
python test_api.py
```

### Manual Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Create a photo
curl -X POST http://localhost:8000/photos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beautiful Sunset",
    "description": "A stunning sunset over the ocean",
    "url": "https://example.com/sunset.jpg",
    "tags": ["sunset", "nature", "ocean"]
  }'

# List all photos
curl http://localhost:8000/photos

# Get a specific photo
curl http://localhost:8000/photos/1

# Update a photo
curl -X PUT http://localhost:8000/photos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Sunset",
    "description": "Updated description",
    "url": "https://example.com/sunset_hd.jpg",
    "tags": ["sunset", "nature"]
  }'

# Delete a photo
curl -X DELETE http://localhost:8000/photos/1
```

## API Endpoints

### Root Endpoint

**GET /**
- Returns API information and available endpoints
- Response: JSON object with API metadata

### Health Check

**GET /health**
- Returns server health status
- Response:
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-01-14T01:00:00.000000",
    "photos_count": 5
  }
  ```

### List Photos

**GET /photos**
- Lists all photos
- Optional query parameter: `tag` (filter by tag)
- Response: Array of photo objects

Example:
```bash
GET /photos?tag=nature
```

### Get Photo

**GET /photos/{photo_id}**
- Retrieves a specific photo by ID
- Returns 404 if photo not found
- Response: Photo object

### Create Photo

**POST /photos**
- Creates a new photo entry
- Request body (JSON):
  ```json
  {
    "title": "string (required)",
    "description": "string (optional)",
    "url": "string (required)",
    "tags": ["array of strings (optional)"]
  }
  ```
- Response: Created photo object with ID and timestamp (201 Created)

### Update Photo

**PUT /photos/{photo_id}**
- Updates an existing photo
- Request body: Same as POST /photos
- Returns 404 if photo not found
- Response: Updated photo object

### Delete Photo

**DELETE /photos/{photo_id}**
- Deletes a photo by ID
- Returns 404 if photo not found
- Response:
  ```json
  {
    "message": "Photo {id} deleted successfully",
    "deleted_photo": {...}
  }
  ```

## Data Models

### Photo (Request)
```json
{
  "title": "string",
  "description": "string | null",
  "url": "string",
  "tags": ["string"]
}
```

### PhotoResponse (Response)
```json
{
  "id": "integer",
  "title": "string",
  "description": "string | null",
  "url": "string",
  "tags": ["string"],
  "created_at": "string (ISO 8601 format)"
}
```

## Interactive API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation where you can test endpoints directly from your browser.

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET, PUT, DELETE operations
- `201 Created`: Successful POST operation
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Invalid request data

Error responses include a detail message:
```json
{
  "detail": "Photo with id 123 not found"
}
```

## Storage

**Note**: This implementation uses in-memory storage. All data will be lost when the server restarts. For production use, integrate a proper database (PostgreSQL, MongoDB, etc.).

## Future Enhancements

Potential improvements for production use:

1. Database integration (SQLAlchemy + PostgreSQL)
2. Authentication and authorization
3. Image upload functionality
4. Pagination for photo listing
5. Search functionality
6. Rate limiting
7. CORS configuration
8. Photo metadata (size, dimensions, EXIF data)
9. User management
10. Comments and likes functionality
