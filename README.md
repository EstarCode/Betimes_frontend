# Betimes
### Enterprise PDF & Document Processing Platform

> Professional document management and processing system

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

**Betimes** is a production-ready document processing platform with comprehensive PDF manipulation, format conversion, and enterprise security features.

## Features

### PDF Operations
- **Merge** - Combine multiple PDFs into one
- **Split** - By pages, ranges, or bookmarks
- **Compress** - Up to 90% size reduction (3 quality levels)
- **Rotate/Delete/Reorder** - Complete page manipulation
- **Watermark** - Text and image watermarks with opacity control
- **Security** - Password protection with AES-256 encryption
- **Extract** - Text, images, tables, and metadata

### Document Conversion
- Word ↔ PDF (bidirectional)
- Excel ↔ PDF (with table preservation)
- PowerPoint ↔ PDF (slide-by-slide)
- Image ↔ PDF (JPG, PNG, TIFF)
- OCR for scanned documents (Tesseract)

### Enterprise Features
- **No Signup Required** - Use freely without registration
- **Unlimited File Size** - Process files up to 10GB
- **No Rate Limiting** - Unlimited usage for all users
- **Batch Processing** - Queue management with real-time progress
- **Async Processing** - Celery for background tasks
- **RESTful API** - Comprehensive API with Swagger documentation
- **Modern UI** - Dark/Light mode with responsive design
- **Production Ready** - Enterprise-grade reliability

---

## Technology Stack

**Backend**
- Django 4.2 + Django REST Framework
- Celery + Redis (async processing)
- PyMuPDF, PyPDF2, pdfplumber (PDF processing)
- python-docx, openpyxl, python-pptx (Office formats)
- Ghostscript (compression)
- Tesseract OCR (text recognition)

**Frontend**
- React 18 + TypeScript
- Tailwind CSS + Shadcn/ui
- Redux Toolkit (state management)
- Framer Motion (animations)
- Axios (API client)

---

## Quick Start

### Prerequisites

```bash
Python 3.11+
Node.js 18+
LibreOffice
Ghostscript
Tesseract OCR
Redis (optional, for async processing)
```

### Installation

**Backend Setup:**
```bash
cd backend
python -m venv venv

# Activate virtual environment
venv\Scripts\activate              # Windows
source venv/bin/activate           # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env             # Windows
cp .env.example .env               # Linux/Mac

# Initialize database
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

**Frontend Setup:**
```bash
cd frontend
npm install

# Configure environment
copy .env.example .env             # Windows
cp .env.example .env               # Linux/Mac

# Edit .env and set:
# VITE_API_URL=http://localhost:8000/api
```

### Run Application

**Development Mode:**
```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate              # Windows
source venv/bin/activate           # Linux/Mac
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm run dev
```

**With Async Processing (Optional):**
```bash
# Terminal 3: Redis
redis-server

# Terminal 4: Celery Worker
cd backend
venv\Scripts\activate
celery -A config worker --loglevel=info --pool=solo
```

### Access Application

- **Frontend:** http://localhost:5173
- **API Documentation:** http://localhost:8000/api/docs/
- **Admin Panel:** http://localhost:8000/admin/

---

## Project Structure

```
betimes/
├── backend/
│   ├── apps/
│   │   ├── authentication/      # User management & JWT
│   │   ├── pdf_tools/           # PDF operations
│   │   ├── conversion/          # Format conversion
│   │   ├── compression/         # PDF compression
│   │   └── analytics/           # Usage tracking
│   ├── config/                  # Django configuration
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Application pages
│   │   ├── services/            # API services
│   │   └── store/               # Redux state
│   ├── package.json
│   └── tsconfig.json
│
├── docs/
│   ├── DEPLOYMENT.md           # Deployment guide
│   └── API.md                  # API documentation
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## API Endpoints

### Authentication
```
POST   /api/auth/register/        # User registration
POST   /api/auth/login/           # User login
POST   /api/auth/token/refresh/   # Refresh token
```

### PDF Operations
```
POST   /api/pdf/merge/            # Merge multiple PDFs
POST   /api/pdf/split/            # Split PDF by pages/ranges
POST   /api/pdf/rotate/           # Rotate pages
POST   /api/pdf/delete-pages/     # Delete specific pages
POST   /api/pdf/reorder/          # Reorder pages
POST   /api/pdf/watermark/        # Add watermark
POST   /api/pdf/password/add/     # Add password protection
POST   /api/pdf/password/remove/  # Remove password
POST   /api/pdf/extract/text/     # Extract text
POST   /api/pdf/extract/images/   # Extract images
GET    /api/pdf/metadata/{id}/    # Get metadata
```

### Document Conversion
```
POST   /api/convert/word-to-pdf/
POST   /api/convert/pdf-to-word/
POST   /api/convert/excel-to-pdf/
POST   /api/convert/pdf-to-excel/
POST   /api/convert/ppt-to-pdf/
POST   /api/convert/pdf-to-ppt/
POST   /api/convert/image-to-pdf/
POST   /api/convert/pdf-to-images/
POST   /api/convert/ocr/
```

### Compression
```
POST   /api/compress/             # Compress PDF
GET    /api/compress/jobs/        # List compression jobs
GET    /api/compress/jobs/{id}/   # Job status
```

**Complete API documentation available at:** `/api/docs/`

---

## Configuration

### Backend Environment (.env)
```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# File Upload
MAX_UPLOAD_SIZE=524288000

# External Tools
GHOSTSCRIPT_PATH=/usr/bin/gs
LIBREOFFICE_PATH=/usr/bin/soffice

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Environment (.env)
```bash
VITE_API_URL=http://localhost:8000/api
```

---

## Testing

```bash
# Backend Tests
cd backend
python manage.py test

# Frontend Tests
cd frontend
npm test

# Coverage Report
cd backend
coverage run --source='.' manage.py test
coverage report
```

---

## Documentation

- **[Deployment Guide](docs/DEPLOYMENT.md)** - Complete deployment instructions for Render and Vercel
- **[API Documentation](docs/API.md)** - Full API reference with examples
- **[Interactive API Docs](http://localhost:8000/api/docs/)** - Swagger UI (when running locally)

---

## Deployment

### Backend Deployment (Render)

1. **Create Render Account** at https://render.com

2. **Create New Web Service**
   - Connect your GitHub repository
   - Select `backend` as root directory
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi:application`

3. **Add Environment Variables** in Render Dashboard:
   ```
   PYTHON_VERSION=3.11.0
   DEBUG=False
   SECRET_KEY=<generate-secure-key>
   ALLOWED_HOSTS=.onrender.com
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```

4. **Add PostgreSQL Database**
   - Create PostgreSQL database in Render
   - Copy `DATABASE_URL` to environment variables

5. **Add Redis** (Optional for async processing)
   - Create Redis instance in Render
   - Copy `REDIS_URL` to environment variables

### Frontend Deployment (Vercel)

1. **Create Vercel Account** at https://vercel.com

2. **Import Project**
   - Connect your GitHub repository
   - Select `frontend` as root directory
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Add Environment Variables** in Vercel Dashboard:
   ```
   VITE_API_URL=https://your-backend.onrender.com/api
   ```

4. **Deploy**
   - Click Deploy
   - Vercel will auto-deploy on every push to main branch

### Post-Deployment

1. Update `CORS_ALLOWED_ORIGINS` in Render with your Vercel URL
2. Update `VITE_API_URL` in Vercel with your Render backend URL
3. Test all features
4. Monitor logs in both platforms

---

## Security

- **Authentication:** JWT with refresh tokens
- **Authorization:** Role-based access control (RBAC)
- **Encryption:** AES-256 for password-protected PDFs
- **Rate Limiting:** API throttling to prevent abuse
- **Input Validation:** Comprehensive request validation
- **Audit Logging:** Complete operation tracking
- **HTTPS:** SSL/TLS support for production
- **File Validation:** Type and size checking
- **Secure Storage:** Automatic temporary file cleanup

---

## Performance

- **Compression:** Up to 90% PDF size reduction
- **Async Processing:** Background task handling with Celery
- **Caching:** Redis caching for improved response times
- **Batch Operations:** Process multiple documents simultaneously
- **Optimized Queries:** Database query optimization
- **CDN Ready:** Static file serving optimization

---

## System Requirements

### Development
- Python 3.11 or higher
- Node.js 18 or higher
- 4GB RAM minimum
- 10GB disk space

### Production
- Python 3.11 or higher
- PostgreSQL 15 or higher
- Redis 7 or higher
- 8GB RAM minimum
- 50GB disk space

---

## Troubleshooting

### Backend Issues

**Dependencies installation fails:**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Database errors:**
```bash
python manage.py migrate --run-syncdb
```

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Frontend Issues

**Dependencies installation fails:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
npm run build
```

### External Tools

**LibreOffice not found:**
```bash
# Update .env with correct path
# Windows: LIBREOFFICE_PATH=C:\Program Files\LibreOffice\program\soffice.exe
# Linux: LIBREOFFICE_PATH=/usr/bin/soffice
```

**Ghostscript not found:**
```bash
# Update .env with correct path
# Windows: GHOSTSCRIPT_PATH=C:\Program Files\gs\gs10.02.1\bin\gswin64c.exe
# Linux: GHOSTSCRIPT_PATH=/usr/bin/gs
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

---

## License

MIT License - see [LICENSE](LICENSE) file for details

---

## Support

For issues and questions:
- Check logs: `backend/logs/django.log`
- Review API docs: http://localhost:8000/api/docs/
- Verify dependencies are installed correctly

---

**DocuForge Enterprise** - Professional Document Processing Platform  
*Built with modern technologies for enterprise reliability*

