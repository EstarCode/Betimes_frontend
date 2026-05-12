# API Documentation

Base URL: `https://your-backend.onrender.com/api`

## Authentication

### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "user@example.com",
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "securepassword123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## PDF Operations

All PDF endpoints require authentication. Include token in header:
```
Authorization: Bearer <access_token>
```

### Merge PDFs
```http
POST /api/pdf/merge/
Content-Type: multipart/form-data

files: [file1.pdf, file2.pdf, file3.pdf]
```

### Split PDF
```http
POST /api/pdf/split/
Content-Type: multipart/form-data

file: document.pdf
split_type: "pages" | "ranges" | "bookmarks"
page_ranges: [[1,5], [6,10]]  # Optional, for ranges
```

### Rotate Pages
```http
POST /api/pdf/rotate/
Content-Type: multipart/form-data

file: document.pdf
rotation: 90 | 180 | 270
pages: [0, 2, 4]  # Optional, rotates all if not specified
```

### Delete Pages
```http
POST /api/pdf/delete-pages/
Content-Type: multipart/form-data

file: document.pdf
pages: [1, 3, 5]  # Pages to delete (0-indexed)
```

### Reorder Pages
```http
POST /api/pdf/reorder/
Content-Type: multipart/form-data

file: document.pdf
new_order: [2, 0, 1, 3]  # New page order (0-indexed)
```

### Add Watermark
```http
POST /api/pdf/watermark/
Content-Type: multipart/form-data

file: document.pdf
watermark_text: "CONFIDENTIAL"
opacity: 0.3  # 0.0 to 1.0
```

### Add Password
```http
POST /api/pdf/password/add/
Content-Type: multipart/form-data

file: document.pdf
user_password: "userpass123"
owner_password: "ownerpass123"  # Optional
```

### Remove Password
```http
POST /api/pdf/password/remove/
Content-Type: multipart/form-data

file: document.pdf
password: "currentpassword"
```

### Extract Text
```http
POST /api/pdf/extract/text/
Content-Type: multipart/form-data

file: document.pdf

Response:
{
  "pages_processed": 10,
  "content": [
    {"page": 1, "text": "Page 1 content..."},
    {"page": 2, "text": "Page 2 content..."}
  ],
  "total_characters": 5000
}
```

### Extract Images
```http
POST /api/pdf/extract/images/
Content-Type: multipart/form-data

file: document.pdf

Response:
{
  "images_extracted": 5,
  "output_files": ["image1.png", "image2.jpg", ...]
}
```

### Get Metadata
```http
GET /api/pdf/metadata/{job_id}/

Response:
{
  "page_count": 10,
  "file_size": 1024000,
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "subject": "Subject",
    "creator": "Creator App"
  },
  "is_encrypted": false
}
```

---

## Document Conversion

### Word to PDF
```http
POST /api/convert/word-to-pdf/
Content-Type: multipart/form-data

file: document.docx
```

### PDF to Word
```http
POST /api/convert/pdf-to-word/
Content-Type: multipart/form-data

file: document.pdf
```

### Excel to PDF
```http
POST /api/convert/excel-to-pdf/
Content-Type: multipart/form-data

file: spreadsheet.xlsx
```

### PDF to Excel
```http
POST /api/convert/pdf-to-excel/
Content-Type: multipart/form-data

file: document.pdf
```

### PowerPoint to PDF
```http
POST /api/convert/ppt-to-pdf/
Content-Type: multipart/form-data

file: presentation.pptx
```

### PDF to PowerPoint
```http
POST /api/convert/pdf-to-ppt/
Content-Type: multipart/form-data

file: document.pdf
```

### Image to PDF
```http
POST /api/convert/image-to-pdf/
Content-Type: multipart/form-data

file: image.jpg
```

### PDF to Images
```http
POST /api/convert/pdf-to-images/
Content-Type: multipart/form-data

file: document.pdf
format: "PNG" | "JPG"
dpi: 200  # Optional, default 200
```

### OCR
```http
POST /api/convert/ocr/
Content-Type: multipart/form-data

file: scanned.pdf
language: "eng"  # Optional, default "eng"
```

---

## Compression

### Compress PDF
```http
POST /api/compress/
Content-Type: multipart/form-data

file: document.pdf
compression_level: "low" | "medium" | "high"

Response:
{
  "job_id": "abc123",
  "status": "processing"
}
```

### Get Compression Jobs
```http
GET /api/compress/jobs/

Response:
{
  "count": 10,
  "results": [
    {
      "id": "abc123",
      "filename": "document.pdf",
      "status": "completed",
      "original_size": 5000000,
      "compressed_size": 500000,
      "compression_ratio": 90.0,
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### Get Job Status
```http
GET /api/compress/jobs/{job_id}/

Response:
{
  "id": "abc123",
  "filename": "document.pdf",
  "status": "completed",
  "original_size": 5000000,
  "compressed_size": 500000,
  "compression_ratio": 90.0,
  "download_url": "/media/compressed/document.pdf",
  "created_at": "2024-01-01T12:00:00Z"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid file format",
  "detail": "Only PDF files are allowed"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Processing failed",
  "detail": "An error occurred while processing your request"
}
```

---

## Rate Limiting

- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640000000
```

---

## Interactive Documentation

Visit these URLs for interactive API documentation:

- **Swagger UI:** `https://your-backend.onrender.com/api/docs/`
- **ReDoc:** `https://your-backend.onrender.com/api/redoc/`
