# Betimes Enterprise Platform - API Documentation

## Base URL

- **Production**: `https://betimes.onrender.com/api`
- **Development**: `http://localhost:8000/api`

## Interactive Documentation

- **Swagger UI**: https://betimes.onrender.com/api/docs/
- **ReDoc**: https://betimes.onrender.com/api/redoc/

## Authentication

All API requests (except registration and login) require JWT authentication.

### Headers
```http
Authorization: Bearer <access_token>
Content-Type: application/json
Accept: application/json
```

---

## Authentication Endpoints

### User Registration
```http
POST /auth/register/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "Viewer"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "Viewer",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### User Login
```http
POST /auth/login/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "Viewer",
    "mfa_enabled": false
  }
}
```

---

### Refresh Token
```http
POST /auth/token/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### User Logout
```http
POST /auth/logout/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

---

### Get User Profile
```http
GET /auth/profile/
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "Viewer",
  "mfa_enabled": false,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-15T10:30:00Z"
}
```

---

### Update User Profile
```http
PATCH /auth/profile/
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith"
}
```

**Response:** `200 OK`

---

### Change Password
```http
POST /auth/change-password/
```

**Request Body:**
```json
{
  "old_password": "OldPassword123!",
  "new_password": "NewPassword456!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password changed successfully"
}
```

---

### Request Password Reset
```http
POST /auth/password-reset/
```

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password reset email sent"
}
```

---

### Confirm Password Reset
```http
POST /auth/password-reset/confirm/
```

**Request Body:**
```json
{
  "token": "reset-token-from-email",
  "new_password": "NewPassword456!"
}
```

**Response:** `200 OK`

---

## Multi-Factor Authentication (MFA)

### Enable MFA
```http
POST /auth/mfa/enable/
```

**Response:** `200 OK`
```json
{
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...",
  "secret": "JBSWY3DPEHPK3PXP",
  "issuer": "Betimes Enterprise"
}
```

---

### Verify MFA Setup
```http
POST /auth/mfa/verify/
```

**Request Body:**
```json
{
  "code": "123456"
}
```

**Response:** `200 OK`
```json
{
  "message": "MFA enabled successfully",
  "backup_codes": [
    "12345678",
    "23456789",
    "34567890",
    "45678901",
    "56789012",
    "67890123",
    "78901234",
    "89012345",
    "90123456",
    "01234567"
  ]
}
```

---

### Disable MFA
```http
POST /auth/mfa/disable/
```

**Request Body:**
```json
{
  "password": "CurrentPassword123!"
}
```

**Response:** `200 OK`

---

### Verify MFA Code (During Login)
```http
POST /auth/mfa/verify-login/
```

**Request Body:**
```json
{
  "code": "123456"
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Regenerate Backup Codes
```http
POST /auth/mfa/regenerate-backup-codes/
```

**Response:** `200 OK`
```json
{
  "backup_codes": [
    "12345678",
    "23456789",
    ...
  ]
}
```

---

## Session Management

### Get Active Sessions
```http
GET /auth/sessions/
```

**Response:** `200 OK`
```json
{
  "sessions": [
    {
      "id": "uuid",
      "device": "Chrome on Windows",
      "ip_address": "192.168.1.1",
      "location": "New York, US",
      "last_activity": "2024-01-15T10:30:00Z",
      "is_current": true
    }
  ]
}
```

---

### Revoke Specific Session
```http
DELETE /auth/sessions/{session_id}/
```

**Response:** `204 No Content`

---

### Revoke All Sessions
```http
POST /auth/sessions/revoke-all/
```

**Response:** `200 OK`
```json
{
  "message": "All sessions revoked successfully",
  "revoked_count": 3
}
```

---

## Document Upload

### Initialize Chunked Upload
```http
POST /uploads/initialize/
```

**Request Body:**
```json
{
  "filename": "document.pdf",
  "file_size": 104857600,
  "content_type": "application/pdf",
  "chunk_size": 5242880
}
```

**Response:** `201 Created`
```json
{
  "upload_id": "uuid",
  "chunk_size": 5242880,
  "total_chunks": 20
}
```

---

### Upload File Chunk
```http
POST /uploads/{upload_id}/chunk/
```

**Request Body:** `multipart/form-data`
- `chunk`: File chunk (binary)
- `chunk_index`: Integer (0-based)

**Response:** `200 OK`
```json
{
  "chunk_index": 0,
  "uploaded": true,
  "progress": 5.0
}
```

---

### Complete Chunked Upload
```http
POST /uploads/{upload_id}/complete/
```

**Response:** `200 OK`
```json
{
  "upload_id": "uuid",
  "file_id": "uuid",
  "filename": "document.pdf",
  "file_size": 104857600,
  "status": "completed"
}
```

---

### Simple Upload (Small Files)
```http
POST /uploads/simple/
```

**Request Body:** `multipart/form-data`
- `file`: File (binary)

**Response:** `201 Created`
```json
{
  "file_id": "uuid",
  "filename": "document.pdf",
  "file_size": 1048576,
  "status": "completed"
}
```

---

### Get Upload Status
```http
GET /uploads/{upload_id}/status/
```

**Response:** `200 OK`
```json
{
  "upload_id": "uuid",
  "status": "in_progress",
  "progress": 45.5,
  "chunks_uploaded": 9,
  "total_chunks": 20
}
```

---

### List All Uploads
```http
GET /uploads/?status=completed&page=1
```

**Response:** `200 OK`
```json
{
  "count": 100,
  "next": "/uploads/?page=2",
  "previous": null,
  "results": [
    {
      "upload_id": "uuid",
      "filename": "document.pdf",
      "file_size": 104857600,
      "status": "completed",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

### Delete Upload
```http
DELETE /uploads/{upload_id}/
```

**Response:** `204 No Content`

---

## Document Conversion

### Convert Document
```http
POST /convert/
```

**Request Body:** `multipart/form-data`
- `file`: File (binary)
- `target_format`: String (pdf, docx, jpg, png)
- `quality`: String (optional: low, medium, high)
- `dpi`: Integer (optional: 72, 150, 300)

**Response:** `202 Accepted`
```json
{
  "job_id": "uuid",
  "status": "pending",
  "source_format": "docx",
  "target_format": "pdf"
}
```

---

### Perform OCR
```http
POST /convert/ocr/
```

**Request Body:** `multipart/form-data`
- `file`: File (binary)
- `language`: String (optional: eng, spa, fra, deu, chi_sim, jpn, ara)
- `output_format`: String (optional: pdf, txt)

**Response:** `202 Accepted`
```json
{
  "job_id": "uuid",
  "status": "pending",
  "language": "eng"
}
```

---

### Batch Convert
```http
POST /convert/batch/
```

**Request Body:** `multipart/form-data`
- `files`: Multiple files (binary)
- `target_format`: String

**Response:** `202 Accepted`
```json
{
  "batch_id": "uuid",
  "job_ids": ["uuid1", "uuid2", "uuid3"],
  "total_files": 3
}
```

---

### Get Supported Formats
```http
GET /convert/formats/
```

**Response:** `200 OK`
```json
{
  "formats": {
    "pdf": ["docx", "jpg", "png"],
    "docx": ["pdf"],
    "jpg": ["pdf"],
    "png": ["pdf"]
  }
}
```

---

### Get Conversion Job Status
```http
GET /convert/jobs/{job_id}/
```

**Response:** `200 OK`
```json
{
  "job_id": "uuid",
  "status": "completed",
  "progress": 100,
  "source_format": "docx",
  "target_format": "pdf",
  "created_at": "2024-01-15T10:00:00Z",
  "completed_at": "2024-01-15T10:02:30Z"
}
```

---

### Download Converted File
```http
GET /convert/jobs/{job_id}/download/
```

**Response:** `200 OK` (Binary file)

---

### Delete Conversion Job
```http
DELETE /convert/jobs/{job_id}/
```

**Response:** `204 No Content`

---

## PDF Tools

### Split PDF by Range
```http
POST /pdf-tools/split/range/
```

**Request Body:** `multipart/form-data`
- `file`: PDF file (binary)
- `ranges`: JSON string `[{"start": 1, "end": 5}, {"start": 10, "end": 15}]`

**Response:** `202 Accepted`
```json
{
  "job_id": "uuid",
  "status": "pending",
  "operation": "split_range",
  "output_files": 2
}
```

---

### Split PDF by Bookmarks
```http
POST /pdf-tools/split/bookmarks/
```

**Request Body:** `multipart/form-data`
- `file`: PDF file (binary)
- `level`: Integer (default: 1)

**Response:** `202 Accepted`

---

### Merge PDFs
```http
POST /pdf-tools/merge/
```

**Request Body:** `multipart/form-data`
- `files`: Multiple PDF files (binary, max 100)
- `add_toc`: Boolean (optional)
- `add_page_numbers`: Boolean (optional)
- `output_filename`: String (optional)

**Response:** `202 Accepted`
```json
{
  "job_id": "uuid",
  "status": "pending",
  "operation": "merge",
  "input_files": 5
}
```

---

### Extract Pages
```http
POST /pdf-tools/extract/
```

**Request Body:** `multipart/form-data`
- `file`: PDF file (binary)
- `pages`: JSON string `[1, 3, 5, 7]`

**Response:** `202 Accepted`

---

### Rotate Pages
```http
POST /pdf-tools/rotate/
```

**Request Body:** `multipart/form-data`
- `file`: PDF file (binary)
- `rotations`: JSON string `{"1": 90, "2": 180, "3": 270}`

**Response:** `202 Accepted`

---

### Reorder Pages
```http
POST /pdf-tools/reorder/
```

**Request Body:** `multipart/form-data`
- `file`: PDF file (binary)
- `order`: JSON string `[3, 1, 2, 5, 4]`

**Response:** `202 Accepted`

---

### Delete Pages
```http
POST /pdf-tools/delete/
```

**Request Body:** `multipart/form-data`
- `file`: PDF file (binary)
- `pages`: JSON string `[2, 4, 6]`

**Response:** `202 Accepted`

---

### Get PDF Information
```http
POST /pdf-tools/info/
```

**Request Body:** `multipart/form-data`
- `file`: PDF file (binary)

**Response:** `200 OK`
```json
{
  "page_count": 10,
  "file_size": 1048576,
  "title": "Document Title",
  "author": "John Doe",
  "created_at": "2024-01-01T00:00:00Z",
  "modified_at": "2024-01-15T10:00:00Z"
}
```

---

### Get PDF Bookmarks
```http
POST /pdf-tools/bookmarks/
```

**Request Body:** `multipart/form-data`
- `file`: PDF file (binary)

**Response:** `200 OK`
```json
{
  "bookmarks": [
    {
      "title": "Chapter 1",
      "page": 1,
      "level": 1
    },
    {
      "title": "Section 1.1",
      "page": 3,
      "level": 2
    }
  ]
}
```

---

## PDF Compression

### Compress PDF
```http
POST /compress/
```

**Request Body:** `multipart/form-data`
- `file`: PDF file (binary)
- `compression_level`: String (low, medium, high)

**Response:** `202 Accepted`
```json
{
  "job_id": "uuid",
  "status": "pending",
  "compression_level": "medium"
}
```

---

### Get Compression Jobs
```http
GET /compress/jobs/?status=completed
```

**Response:** `200 OK`
```json
{
  "count": 50,
  "results": [
    {
      "job_id": "uuid",
      "status": "completed",
      "original_size": 10485760,
      "compressed_size": 5242880,
      "compression_ratio": 50.0,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

### Get Compression Job Status
```http
GET /compress/jobs/{job_id}/
```

**Response:** `200 OK`

---

### Delete Compression Job
```http
DELETE /compress/jobs/{job_id}/delete/
```

**Response:** `204 No Content`

---

## Search Engine

### Search Documents
```http
GET /search/?q=contract&file_type=pdf&date_from=2024-01-01&page=1
```

**Query Parameters:**
- `q`: Search query (required)
- `file_type`: Filter by file type
- `owner`: Filter by owner
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)
- `min_size`: Minimum file size (bytes)
- `max_size`: Maximum file size (bytes)
- `tags`: Comma-separated tags
- `page`: Page number
- `page_size`: Results per page

**Response:** `200 OK`
```json
{
  "count": 100,
  "results": [
    {
      "id": "uuid",
      "filename": "contract.pdf",
      "file_type": "pdf",
      "file_size": 1048576,
      "owner": "user@example.com",
      "created_at": "2024-01-15T10:00:00Z",
      "relevance_score": 0.95
    }
  ]
}
```

---

### Advanced Search
```http
POST /search/advanced/
```

**Request Body:**
```json
{
  "query": "contract",
  "filters": {
    "file_type": ["pdf", "docx"],
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "size_range": {
      "min": 1024,
      "max": 10485760
    },
    "tags": ["legal", "important"]
  },
  "sort_by": "relevance",
  "page": 1,
  "page_size": 20
}
```

**Response:** `200 OK`

---

### Get Search Suggestions
```http
GET /search/suggestions/?q=cont
```

**Response:** `200 OK`
```json
{
  "suggestions": [
    "contract",
    "content",
    "contractor",
    "continue"
  ]
}
```

---

### Get Search History
```http
GET /search/history/?limit=10
```

**Response:** `200 OK`
```json
{
  "history": [
    {
      "query": "contract",
      "timestamp": "2024-01-15T10:00:00Z",
      "results_count": 25
    }
  ]
}
```

---

### Clear Search History
```http
DELETE /search/history/
```

**Response:** `204 No Content`

---

### Save Search Query
```http
POST /search/saved/
```

**Request Body:**
```json
{
  "name": "Legal Contracts",
  "query": {
    "q": "contract",
    "file_type": "pdf",
    "tags": ["legal"]
  }
}
```

**Response:** `201 Created`

---

### Get Saved Searches
```http
GET /search/saved/
```

**Response:** `200 OK`

---

### Delete Saved Search
```http
DELETE /search/saved/{search_id}/
```

**Response:** `204 No Content`

---

### Get Popular Searches
```http
GET /search/popular/?limit=10
```

**Response:** `200 OK`
```json
{
  "popular": [
    {
      "query": "contract",
      "count": 150
    },
    {
      "query": "invoice",
      "count": 120
    }
  ]
}
```

---

## Health & Monitoring

### Basic Health Check
```http
GET /health/
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

---

### Readiness Check
```http
GET /health/ready/
```

**Response:** `200 OK`
```json
{
  "status": "ready",
  "database": "connected",
  "redis": "connected",
  "celery": "running"
}
```

---

### Liveness Check
```http
GET /health/live/
```

**Response:** `200 OK`
```json
{
  "status": "alive",
  "uptime": 86400
}
```

---

## Error Responses

All errors follow RFC 7807 standard:

```json
{
  "error": {
    "type": "https://betimes.onrender.com/errors/validation-error",
    "title": "Validation Error",
    "status": 400,
    "detail": "Invalid email format",
    "instance": "/api/auth/register/",
    "timestamp": "2024-01-15T10:00:00Z",
    "request_id": "1234567890-abcdef"
  }
}
```

### Common Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `202 Accepted` - Request accepted (async processing)
- `204 No Content` - Success with no response body
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## Rate Limiting

- **Limit**: 100 requests per minute per user
- **Headers**:
  - `X-RateLimit-Limit`: Total requests allowed
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets (Unix timestamp)

---

## Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Results per page (default: 20, max: 100)

**Response:**
```json
{
  "count": 100,
  "next": "/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Filtering & Sorting

**Common Filters:**
- `status`: Filter by status
- `created_at__gte`: Created after date
- `created_at__lte`: Created before date
- `search`: Full-text search

**Sorting:**
- `ordering`: Field name (prefix with `-` for descending)
- Example: `?ordering=-created_at`

---

## Best Practices

1. **Always use HTTPS** in production
2. **Store tokens securely** (never in localStorage for sensitive apps)
3. **Implement token refresh** before expiration
4. **Handle rate limits** gracefully
5. **Use pagination** for large datasets
6. **Validate input** on client side
7. **Handle errors** properly
8. **Log requests** for debugging
9. **Use request IDs** for tracking
10. **Implement retry logic** for failed requests

---

## Support

- **Interactive Docs**: https://betimes.onrender.com/api/docs/
- **Integration Guide**: `frontend/API_INTEGRATION.md`
- **GitHub Issues**: Report bugs and feature requests
