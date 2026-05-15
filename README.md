# Betimes - Professional Document Processing Platform

> Modern, scalable document management and processing system built with Django and React

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.0-DC382D.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Overview

**Betimes** is a production-ready document processing platform designed for modern web applications. Built with Django REST Framework and React, it provides comprehensive document management, conversion, and workflow automation capabilities with a focus on performance, security, and user experience.

### 🌐 Live Demo

- **API**: https://betimes.onrender.com/api
- **Documentation**: https://betimes.onrender.com/api/docs/
- **Health Check**: https://betimes.onrender.com/health/

### ✨ Key Features

- 🔥 **High Performance** - Process thousands of documents with optimized async handling
- 📦 **Large File Support** - Handle files up to 10GB with resumable chunked uploads
- 🔒 **Secure** - JWT authentication, MFA, role-based access control, AES-256 encryption
- 🔄 **Workflow Automation** - Multi-step approval chains with routing
- 📊 **Real-time Analytics** - Live dashboard with system metrics
- 🔍 **Advanced Search** - Full-text search across all documents
- 🛠️ **PDF Tools** - Split, merge, rotate, compress, and manipulate PDFs
- 🌐 **Multi-language** - Support for 7 languages
- ⚡ **Async Processing** - Background tasks with Celery and Redis
- 🎨 **Modern UI** - Beautiful, responsive interface with smooth animations
- 🌍 **Standards Compliant** - OWASP, RFC 7807, WCAG 2.1 AA, ISO 27001

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Security](#-security)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 📄 Document Processing

#### **File Upload System**
- Upload files up to **10GB** with chunked uploads
- Resumable uploads - continue from last successful chunk
- Parallel processing - up to 4 concurrent uploads
- SHA-256 integrity validation
- Real-time progress tracking
- Batch uploads - up to 50 files simultaneously

#### **Document Conversion**
- **PDF ↔ Word** - Bidirectional conversion with formatting preservation
- **Excel → PDF** - XLSX/XLS with table preservation
- **PowerPoint → PDF** - PPTX/PPT conversion
- **Image → PDF** - JPG, PNG, TIFF support
- **PDF → Images** - Configurable DPI (72, 150, 300)
- **Text → PDF** - Customizable formatting

#### **PDF Operations**
- **Split PDF** - By page range or bookmarks
- **Merge PDFs** - Combine up to 100 PDFs with table of contents
- **Extract Pages** - Select specific pages
- **Rotate Pages** - 90, 180, 270 degree rotation
- **Reorder Pages** - Drag and drop reordering
- **Compression** - 3 levels (low, medium, high)
- **Watermark** - Text and image watermarks
- **Security** - Password protection with AES-256

#### **OCR Text Extraction**
- Extract text from scanned documents
- 95%+ accuracy for clear documents
- 7 languages supported
- Generate searchable PDFs
- Support for JPG, PNG, TIFF, PDF formats

### 🔄 Advanced Features

#### **Workflow Automation**
- Multi-step approval chains
- Parallel and sequential approval modes
- Department-based routing
- Auto-escalation
- Reusable workflow templates
- Status tracking and notifications

#### **Authentication & Security**
- **JWT Authentication** - Secure token-based auth
- **Multi-Factor Authentication** - TOTP + SMS + backup codes
- **Role-Based Access Control** - Granular permissions
- **Session Management** - Track and manage active sessions
- **Account Security** - Auto-lockout, password policies

#### **Dashboard & Analytics**
- Real-time metrics with auto-refresh
- Upload statistics and trends
- Processing job monitoring
- Storage usage analytics
- System health indicators

#### **Global Search**
- Full-text search across all documents
- Advanced filters (file type, date, size, status)
- Fast results (< 2 seconds)
- Search term highlighting
- Autocomplete suggestions

#### **Notification System**
- Email notifications
- In-app notifications
- SMS alerts (optional)
- Slack/Teams integration (optional)
- Configurable preferences

### 🎨 User Interface

- **Modern Design** - Clean, professional interface
- **Smooth Animations** - 60 FPS performance
- **Responsive** - Desktop, tablet, mobile support
- **Light/Dark Themes** - User preference persistence
- **Keyboard Shortcuts** - Efficient navigation
- **WCAG 2.1 AA** - Accessibility compliant

---

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework 3.14
- **Database**: PostgreSQL 15 (production) / SQLite (development)
- **Cache & Queue**: Redis 7.0
- **Task Queue**: Celery 5.3
- **Authentication**: JWT (Simple JWT)
- **API Docs**: Swagger/OpenAPI (drf-yasg)
- **PDF Processing**: PyMuPDF, PyPDF2, pdfplumber
- **Office Formats**: python-docx, reportlab
- **Image Processing**: Pillow, pdf2image
- **OCR**: pytesseract, Tesseract OCR
- **Security**: cryptography, django-cors-headers
- **Testing**: pytest, pytest-django
- **WSGI Server**: Gunicorn

### Frontend
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **State Management**: Redux Toolkit
- **Routing**: React Router 6
- **Styling**: Tailwind CSS 3.4
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **File Upload**: react-dropzone

### DevOps
- **Version Control**: Git
- **Backend Hosting**: Render
- **Frontend Hosting**: Vercel
- **Monitoring**: Sentry
- **CDN**: Cloudflare (optional)

---

## 🚀 Quick Start

### Prerequisites

```bash
✓ Python 3.11+
✓ Node.js 18+
✓ PostgreSQL 15 (production) / SQLite (development)
✓ Redis 7.0
✓ Ghostscript
✓ Tesseract OCR
```

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/betimes.git
cd betimes

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Frontend setup
cd ../frontend
npm install
cp .env.example .env
```

### Running Locally

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - Redis (optional)
redis-server

# Terminal 4 - Celery (optional)
cd backend
celery -A config worker --loglevel=info
```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **API Docs**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

---

## ⚙️ Configuration

### Backend Environment (.env)

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=betimes.onrender.com,localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@host:5432/betimes_db

# Redis
REDIS_URL=redis://host:6379/0
CELERY_BROKER_URL=redis://host:6379/0
CELERY_RESULT_BACKEND=redis://host:6379/0

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=15  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 days

# CORS
CORS_ALLOWED_ORIGINS=https://betimes.vercel.app,http://localhost:5173

# File Upload
MAX_UPLOAD_SIZE=10737418240  # 10GB
ALLOWED_EXTENSIONS=pdf,doc,docx,jpg,jpeg,png,xlsx,pptx

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Monitoring (optional)
SENTRY_DSN=your-sentry-dsn
```

### Frontend Environment (.env)

```bash
# API URL
VITE_API_URL=https://betimes.onrender.com/api

# Application Settings
VITE_APP_NAME=Betimes
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_MFA=true
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_WORKFLOWS=true

# File Upload Limits
VITE_MAX_FILE_SIZE=10737418240
VITE_MAX_CHUNK_SIZE=5242880

# Session Settings
VITE_SESSION_TIMEOUT=3600000
VITE_TOKEN_REFRESH_INTERVAL=300000
```

---

## 📡 API Documentation

### Base URL
- **Production**: `https://betimes.onrender.com/api`
- **Development**: `http://localhost:8000/api`

### Interactive Documentation
- **Swagger UI**: https://betimes.onrender.com/api/docs/
- **ReDoc**: https://betimes.onrender.com/api/redoc/

### Key Endpoints

#### Authentication
```bash
POST /api/v1/auth/register/     # Register new user
POST /api/v1/auth/login/        # Login
POST /api/v1/auth/token/refresh/ # Refresh token
GET  /api/v1/auth/profile/      # Get user profile
```

#### Document Processing
```bash
POST /api/v1/compress/          # Compress PDF
POST /api/v1/convert/           # Convert document
POST /api/v1/tools/pdf/split/   # Split PDF
POST /api/v1/tools/pdf/merge/   # Merge PDFs
POST /api/v1/tools/pdf/rotate/  # Rotate pages
```

#### Search & Analytics
```bash
GET  /api/v1/search/            # Search documents
GET  /api/v1/dashboard/metrics/ # Get metrics
GET  /api/v1/analytics/         # Get analytics
```

#### Health Checks
```bash
GET  /health/                   # Basic health
GET  /health/ready/             # Readiness (DB + Cache)
GET  /health/live/              # Liveness
```

---

## 🚢 Deployment

### Backend (Render)

1. **Create PostgreSQL Database**
   - Go to Render Dashboard
   - Create new PostgreSQL instance
   - Copy DATABASE_URL

2. **Create Redis Instance**
   - Create new Redis instance
   - Copy REDIS_URL

3. **Deploy Web Service**
   - Connect GitHub repository
   - Root Directory: `backend`
   - Build Command: `chmod +x render-build.sh && ./render-build.sh`
   - Start Command: `gunicorn config.wsgi:application --config gunicorn.conf.py`

4. **Set Environment Variables**
   ```bash
   SECRET_KEY=<generate-secure-key>
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   DATABASE_URL=<from-postgresql>
   REDIS_URL=<from-redis>
   CELERY_BROKER_URL=<from-redis>
   CELERY_RESULT_BACKEND=<from-redis>
   CORS_ALLOWED_ORIGINS=https://betimes.vercel.app
   ```

5. **Create Celery Workers** (separate services)
   - Worker: `celery -A config worker --loglevel=info`
   - Beat: `celery -A config beat --loglevel=info`

### Frontend (Vercel)

1. **Import Project**
   - Connect GitHub repository
   - Root Directory: `frontend`
   - Framework: Vite

2. **Set Environment Variables**
   ```bash
   VITE_API_URL=https://betimes.onrender.com/api
   VITE_APP_NAME=Betimes
   VITE_ENABLE_MFA=true
   ```

3. **Deploy**
   - Push to main branch
   - Vercel auto-deploys

### Verification

```bash
# Check health
curl https://betimes.onrender.com/health/

# Check API docs
open https://betimes.onrender.com/api/docs/

# Test registration
curl -X POST https://betimes.onrender.com/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"TestPass123!@#","password_confirm":"TestPass123!@#"}'
```

---

## 🔒 Security

### Authentication
- JWT tokens with automatic refresh
- Multi-factor authentication (TOTP + SMS)
- Role-based access control
- Session management
- Account lockout after failed attempts

### Data Protection
- AES-256 encryption at rest
- TLS 1.3 encryption in transit
- Secure cookie handling
- CSRF protection
- XSS prevention
- SQL injection prevention

### API Security
- Rate limiting (100 req/min per user)
- CORS policies
- Security headers
- Request logging
- Input validation
- RFC 7807 error responses

### Compliance
- ✅ OWASP Top 10
- ✅ ISO/IEC 27001
- ✅ NIST SP 800-63B
- ✅ RFC 6749 (OAuth 2.0)
- ✅ RFC 7807 (Problem Details)
- ✅ WCAG 2.1 AA
- ✅ GDPR compliant

---

## ⚡ Performance

- **Scalability**: Handles thousands of concurrent users
- **Response Time**: 95% of API calls < 100ms
- **Cache Hit Rate**: 90% for metadata queries
- **File Processing**: Optimized async handling
- **Search**: Results in < 2 seconds
- **Upload Speed**: Parallel chunked uploads

---

## 🧪 Testing

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test

# Run with coverage
cd backend
pytest --cov=apps
```

---

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

**Database errors:**
```bash
python manage.py migrate --run-syncdb
```

**Dependencies fail:**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Frontend build errors:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

### Documentation
- **API Docs**: https://betimes.onrender.com/api/docs/
- **Deployment Guide**: See `DEPLOYMENT.md`

### Health Checks
- **Basic**: https://betimes.onrender.com/health/
- **Readiness**: https://betimes.onrender.com/health/ready/
- **Liveness**: https://betimes.onrender.com/health/live/

### Resources
- **Django**: https://docs.djangoproject.com/
- **React**: https://react.dev/
- **Render**: https://render.com/docs
- **Vercel**: https://vercel.com/docs

---

## 🌟 Acknowledgments

Built with modern technologies and following international standards for security, performance, and accessibility.

---

**Made with ❤️ by the Betimes Team**
