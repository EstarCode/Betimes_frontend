# Design Document: Betimes Enterprise Document Processing Platform

## 1. System Architecture

### 1.1 High-Level Architecture
- **Architecture Pattern**: Microservices with Event-Driven Architecture
- **Communication**: REST APIs + WebSocket for real-time updates
- **Message Queue**: Celery with Redis for async task processing
- **Storage**: Distributed cloud storage (AWS S3/Azure Blob) with local caching
- **Database**: PostgreSQL (primary) with read replicas
- **Cache Layer**: Redis for sessions, metadata, and query results

### 1.2 Core Components
1. **API Gateway**: Nginx reverse proxy with rate limiting
2. **Authentication Service**: JWT + MFA management
3. **Upload Service**: Chunked upload handler with resumption
4. **Processing Service**: Document conversion, compression, OCR
5. **Storage Service**: Encrypted distributed file storage
6. **Workflow Service**: Approval chain management
7. **Notification Service**: Email, SMS, Slack, Teams integration
8. **Search Service**: Full-text search with Elasticsearch
9. **Admin Service**: User and system management
10. **Audit Service**: Compliance logging
11. **Dashboard Service**: Real-time metrics aggregation
12. **Version Control Service**: Document versioning and diff

## 2. Technology Stack

### 2.1 Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Async Tasks**: Celery 5.3 with Redis broker
- **Database**: PostgreSQL 15 with connection pooling (pgBouncer)
- **Cache**: Redis 7.0 (sessions, metadata, search results)
- **Search**: Elasticsearch 8.x for full-text search
- **File Processing**: 
  - PyPDF2, pdf2docx for PDF operations
  - python-docx for Word processing
  - Pillow for image processing
  - Tesseract OCR for text extraction
- **Authentication**: PyJWT, pyotp (TOTP), twilio (SMS)
- **Storage**: boto3 (AWS S3) or azure-storage-blob
- **Monitoring**: Sentry, Prometheus client
- **WSGI Server**: Gunicorn with 4 workers per container

### 2.2 Frontend
- **Framework**: Next.js 14 (React 18)
- **UI Library**: Material-UI v5 with custom glassmorphism theme
- **State Management**: Redux Toolkit + RTK Query
- **File Upload**: Uppy for chunked uploads with resumption
- **Document Viewer**: PDF.js, react-pdf, Mammoth.js (DOCX)
- **Real-time**: Socket.io-client for WebSocket connections
- **Charts**: Recharts for dashboard visualizations
- **Forms**: React Hook Form + Yup validation
- **Internationalization**: next-i18next
- **Performance**: Code splitting, lazy loading, service workers

### 2.3 Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production) or Docker Swarm
- **CI/CD**: GitHub Actions
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Render or AWS ECS
- **Database**: Managed PostgreSQL (AWS RDS/Azure Database)
- **Cache/Queue**: Managed Redis (AWS ElastiCache/Azure Cache)
- **Storage**: AWS S3 or Azure Blob Storage
- **CDN**: CloudFront or Azure CDN
- **Monitoring**: Grafana + Prometheus + ELK Stack

## 3. Database Schema

### 3.1 Users and Authentication
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) NOT NULL CHECK (role IN ('Super_Admin', 'Admin', 'Manager', 'Reviewer', 'Processor', 'Viewer')),
    department VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_secret VARCHAR(32),
    backup_codes TEXT[],
    password_changed_at TIMESTAMP,
    password_history TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_department ON users(department);

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    device_info JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    last_activity TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);

CREATE TABLE login_attempts (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255),
    ip_address INET,
    success BOOLEAN,
    failure_reason VARCHAR(255),
    attempted_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_login_attempts_email_time ON login_attempts(email, attempted_at);
CREATE INDEX idx_login_attempts_ip_time ON login_attempts(ip_address, attempted_at);

### 3.2 Documents and Storage
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(500) NOT NULL,
    original_filename VARCHAR(500) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100),
    checksum_sha256 VARCHAR(64) NOT NULL,
    storage_path TEXT NOT NULL,
    storage_bucket VARCHAR(255),
    encrypted BOOLEAN DEFAULT TRUE,
    encryption_key_id VARCHAR(255),
    owner_id UUID REFERENCES users(id),
    department VARCHAR(100),
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_documents_owner_id ON documents(owner_id);
CREATE INDEX idx_documents_file_type ON documents(file_type);
CREATE INDEX idx_documents_created_at ON documents(created_at);
CREATE INDEX idx_documents_checksum ON documents(checksum_sha256);
CREATE INDEX idx_documents_department ON documents(department);

CREATE TABLE document_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    file_size BIGINT NOT NULL,
    checksum_sha256 VARCHAR(64) NOT NULL,
    storage_path TEXT NOT NULL,
    is_rollback BOOLEAN DEFAULT FALSE,
    rollback_from_version INTEGER,
    modified_by UUID REFERENCES users(id),
    change_description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_document_versions_document_id ON document_versions(document_id);
CREATE INDEX idx_document_versions_version_number ON document_versions(document_id, version_number);

CREATE TABLE upload_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    filename VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    chunk_size INTEGER DEFAULT 10485760,
    total_chunks INTEGER NOT NULL,
    uploaded_chunks INTEGER DEFAULT 0,
    checksum_sha256 VARCHAR(64),
    status VARCHAR(50) DEFAULT 'in_progress',
    storage_temp_path TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
CREATE INDEX idx_upload_sessions_user_id ON upload_sessions(user_id);
CREATE INDEX idx_upload_sessions_status ON upload_sessions(status);

CREATE TABLE upload_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upload_session_id UUID REFERENCES upload_sessions(id) ON DELETE CASCADE,
    chunk_number INTEGER NOT NULL,
    chunk_size INTEGER NOT NULL,
    checksum_sha256 VARCHAR(64),
    storage_path TEXT,
    uploaded_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(upload_session_id, chunk_number)
);
CREATE INDEX idx_upload_chunks_session_id ON upload_chunks(upload_session_id);

### 3.3 Processing Jobs
```sql
CREATE TABLE processing_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_type VARCHAR(50) NOT NULL CHECK (job_type IN ('pdf_to_word', 'word_to_pdf', 'compress', 'split', 'merge', 'ocr', 'convert')),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'queued', 'processing', 'completed', 'failed')),
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('high', 'normal', 'low')),
    user_id UUID REFERENCES users(id),
    input_document_id UUID REFERENCES documents(id),
    output_document_id UUID REFERENCES documents(id),
    parameters JSONB,
    progress_percentage INTEGER DEFAULT 0,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    celery_task_id VARCHAR(255),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_processing_jobs_user_id ON processing_jobs(user_id);
CREATE INDEX idx_processing_jobs_status ON processing_jobs(status);
CREATE INDEX idx_processing_jobs_created_at ON processing_jobs(created_at);
CREATE INDEX idx_processing_jobs_celery_task_id ON processing_jobs(celery_task_id);

### 3.4 Workflows
```sql
CREATE TABLE workflow_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    approval_type VARCHAR(50) CHECK (approval_type IN ('sequential', 'parallel')),
    max_stages INTEGER DEFAULT 10,
    escalation_hours INTEGER DEFAULT 48,
    created_by UUID REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE workflow_stages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID REFERENCES workflow_templates(id) ON DELETE CASCADE,
    stage_number INTEGER NOT NULL,
    stage_name VARCHAR(255) NOT NULL,
    approver_role VARCHAR(50),
    approver_user_id UUID REFERENCES users(id),
    department VARCHAR(100),
    required BOOLEAN DEFAULT TRUE,
    UNIQUE(template_id, stage_number)
);

CREATE TABLE workflow_instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID REFERENCES workflow_templates(id),
    document_id UUID REFERENCES documents(id),
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'pending', 'in_review', 'approved', 'rejected', 'escalated')),
    current_stage INTEGER DEFAULT 1,
    initiated_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
CREATE INDEX idx_workflow_instances_document_id ON workflow_instances(document_id);
CREATE INDEX idx_workflow_instances_status ON workflow_instances(status);

CREATE TABLE workflow_approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_instance_id UUID REFERENCES workflow_instances(id) ON DELETE CASCADE,
    stage_number INTEGER NOT NULL,
    approver_id UUID REFERENCES users(id),
    decision VARCHAR(50) CHECK (decision IN ('approved', 'rejected', 'escalated')),
    comments TEXT,
    decided_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_workflow_approvals_instance_id ON workflow_approvals(workflow_instance_id);

### 3.5 Audit and Compliance
```sql
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    user_id UUID REFERENCES users(id),
    ip_address INET,
    user_agent TEXT,
    resource_type VARCHAR(100),
    resource_id UUID,
    action VARCHAR(100) NOT NULL,
    details JSONB,
    success BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);

### 3.6 Notifications
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    type VARCHAR(50) NOT NULL,
    channel VARCHAR(50) CHECK (channel IN ('email', 'sms', 'in_app', 'slack', 'teams')),
    subject VARCHAR(500),
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'failed')),
    sent_at TIMESTAMP,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);

CREATE TABLE notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) UNIQUE,
    email_enabled BOOLEAN DEFAULT TRUE,
    sms_enabled BOOLEAN DEFAULT FALSE,
    in_app_enabled BOOLEAN DEFAULT TRUE,
    slack_enabled BOOLEAN DEFAULT FALSE,
    teams_enabled BOOLEAN DEFAULT FALSE,
    event_preferences JSONB
);

## 4. API Design

### 4.1 Authentication Endpoints
- POST /api/v1/auth/register - Register new user
- POST /api/v1/auth/login - Login with credentials
- POST /api/v1/auth/logout - Logout current session
- POST /api/v1/auth/refresh - Refresh access token
- POST /api/v1/auth/mfa/setup - Setup MFA
- POST /api/v1/auth/mfa/verify - Verify MFA code
- POST /api/v1/auth/mfa/disable - Disable MFA
- GET /api/v1/auth/sessions - List active sessions
- DELETE /api/v1/auth/sessions/:id - Terminate session
- POST /api/v1/auth/password/change - Change password
- POST /api/v1/auth/password/reset - Request password reset

### 4.2 Document Management Endpoints
- POST /api/v1/documents/upload/init - Initialize chunked upload
- POST /api/v1/documents/upload/chunk - Upload file chunk
- POST /api/v1/documents/upload/complete - Complete upload
- GET /api/v1/documents - List documents (paginated)
- GET /api/v1/documents/:id - Get document details
- GET /api/v1/documents/:id/download - Download document
- DELETE /api/v1/documents/:id - Delete document
- GET /api/v1/documents/:id/versions - List document versions
- POST /api/v1/documents/:id/versions/rollback - Rollback to version
- GET /api/v1/documents/:id/preview - Preview document

### 4.3 Processing Endpoints
- POST /api/v1/processing/pdf-to-word - Convert PDF to Word
- POST /api/v1/processing/word-to-pdf - Convert Word to PDF
- POST /api/v1/processing/compress - Compress PDF
- POST /api/v1/processing/split - Split PDF
- POST /api/v1/processing/merge - Merge PDFs
- POST /api/v1/processing/ocr - Perform OCR
- POST /api/v1/processing/convert - Convert document format
- GET /api/v1/processing/jobs - List processing jobs
- GET /api/v1/processing/jobs/:id - Get job status
- DELETE /api/v1/processing/jobs/:id - Cancel job

### 4.4 Workflow Endpoints
- GET /api/v1/workflows/templates - List workflow templates
- POST /api/v1/workflows/templates - Create workflow template
- PUT /api/v1/workflows/templates/:id - Update workflow template
- DELETE /api/v1/workflows/templates/:id - Delete workflow template
- POST /api/v1/workflows/instances - Create workflow instance
- GET /api/v1/workflows/instances - List workflow instances
- GET /api/v1/workflows/instances/:id - Get workflow details
- POST /api/v1/workflows/instances/:id/approve - Approve workflow stage
- POST /api/v1/workflows/instances/:id/reject - Reject workflow

### 4.5 Search Endpoints
- GET /api/v1/search/documents - Search documents with filters
- GET /api/v1/search/suggest - Get search suggestions

### 4.6 Admin Endpoints
- GET /api/v1/admin/users - List all users
- POST /api/v1/admin/users - Create user
- PUT /api/v1/admin/users/:id - Update user
- DELETE /api/v1/admin/users/:id - Deactivate user
- GET /api/v1/admin/audit-logs - View audit logs
- GET /api/v1/admin/system/health - System health check
- GET /api/v1/admin/system/metrics - System metrics
- PUT /api/v1/admin/system/settings - Update system settings

### 4.7 Dashboard Endpoints
- GET /api/v1/dashboard/metrics - Get dashboard metrics
- GET /api/v1/dashboard/uploads - Upload statistics
- GET /api/v1/dashboard/jobs - Job statistics
- GET /api/v1/dashboard/storage - Storage usage
- GET /api/v1/dashboard/users - User activity

### 4.8 Notification Endpoints
- GET /api/v1/notifications - List user notifications
- PUT /api/v1/notifications/:id/read - Mark notification as read
- PUT /api/v1/notifications/preferences - Update notification preferences

## 5. Security Architecture

### 5.1 Authentication Flow
1. User submits credentials to /api/v1/auth/login
2. Backend validates credentials (bcrypt password hash)
3. If MFA enabled, require TOTP/SMS verification
4. Generate RS256 JWT access token (15 min expiry)
5. Generate RS256 JWT refresh token (7 day expiry)
6. Store session in Redis and PostgreSQL
7. Return tokens to client
8. Client stores tokens in httpOnly cookies or localStorage
9. Include access token in Authorization header for API requests
10. Refresh token when access token expires

### 5.2 Authorization (RBAC)
```python
PERMISSIONS = {
    'Super_Admin': ['*'],  # All permissions
    'Admin': [
        'users.create', 'users.read', 'users.update', 'users.delete',
        'workflows.create', 'workflows.read', 'workflows.update', 'workflows.delete',
        'audit.read', 'system.configure'
    ],
    'Manager': [
        'documents.read', 'documents.create', 'documents.update',
        'workflows.create', 'workflows.read', 'workflows.approve',
        'team.read'
    ],
    'Reviewer': [
        'documents.read', 'workflows.read', 'workflows.approve'
    ],
    'Processor': [
        'documents.create', 'documents.read', 'documents.update',
        'processing.create', 'processing.read'
    ],
    'Viewer': [
        'documents.read'
    ]
}
```

### 5.3 Data Encryption
- **At Rest**: AES-256 encryption for all files in storage
- **In Transit**: TLS 1.3 for all communications
- **Database**: Encrypted columns for sensitive data (passwords, MFA secrets)
- **Key Management**: AWS KMS or Azure Key Vault for encryption keys

### 5.4 Security Headers
```python
SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin'
}
```

### 5.5 Rate Limiting
- 100 requests per minute per user for API endpoints
- 10 requests per minute for authentication endpoints
- 5 failed login attempts trigger 30-minute account lock
- Implemented using Redis with sliding window algorithm

### 5.6 Input Validation
- All user inputs sanitized using bleach library
- Parameterized SQL queries to prevent injection
- File upload validation: type, size, malware scanning
- CSRF tokens for all state-changing operations

## 6. Performance Optimization

### 6.1 Caching Strategy
```python
CACHE_CONFIG = {
    'sessions': {'ttl': 900},  # 15 minutes
    'document_metadata': {'ttl': 300},  # 5 minutes
    'search_results': {'ttl': 120},  # 2 minutes
    'dashboard_metrics': {'ttl': 30},  # 30 seconds
    'user_permissions': {'ttl': 600}  # 10 minutes
}
```

### 6.2 Database Optimization
- Connection pooling: min 10, max 50 connections
- Read replicas for analytics and reporting queries
- Materialized views for dashboard metrics
- Partitioning for audit_logs table by month
- Query optimization with EXPLAIN ANALYZE
- Batch inserts for bulk operations

### 6.3 Async Processing
- All file operations processed asynchronously via Celery
- Separate queues: high_priority, normal, low_priority, cleanup
- Worker auto-scaling based on queue depth
- Job retry with exponential backoff (3 attempts)

### 6.4 File Processing Optimization
- Chunked upload/download (10MB chunks)
- Parallel chunk processing (4 concurrent connections)
- Stream processing for large files
- Lazy loading for document previews
- CDN for static assets and frequently accessed files

### 6.5 Frontend Optimization
- Code splitting by route
- Lazy loading for images and components
- Virtual scrolling for large lists (react-window)
- Service workers for offline capability
- Asset compression (gzip/brotli)
- Image optimization (WebP format)
- Debouncing for search inputs
- Memoization for expensive computations

## 7. Scalability Architecture

### 7.1 Horizontal Scaling
- Stateless API servers (scale to N instances)
- Load balancer (Nginx/AWS ALB) with round-robin
- Celery workers (scale to 20 workers based on queue depth)
- Database read replicas (scale reads)
- Redis cluster for distributed caching

### 7.2 Auto-Scaling Rules
- Scale API servers when CPU > 70% for 5 minutes
- Scale Celery workers when queue depth > 1000 jobs
- Scale down when CPU < 30% for 10 minutes

### 7.3 High Availability
- Multi-AZ deployment for all services
- Database failover with automatic promotion
- Redis Sentinel for cache high availability
- Health checks every 30 seconds
- Automatic instance replacement on failure
- 99.9% uptime SLA

## 8. Monitoring and Observability

### 8.1 Metrics Collection
- Prometheus for metrics scraping
- Grafana for visualization
- Custom metrics:
  - Upload success/failure rate
  - Processing job duration
  - API response times (p50, p95, p99)
  - Queue depth and processing rate
  - Cache hit rate
  - Database query performance

### 8.2 Logging
- Structured logging (JSON format)
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- 90-day retention with searchable indexing
- Correlation IDs for request tracing

### 8.3 Error Tracking
- Sentry for error monitoring and alerting
- Automatic error grouping and deduplication
- Source map support for frontend errors
- Performance monitoring

### 8.4 Alerting Rules
- Upload failure rate > 5%
- API response time p95 > 2 seconds
- Queue processing delay > 10 minutes
- CPU usage > 80% for 5 minutes
- Memory usage > 85%
- Disk usage > 90%
- Database connection pool exhaustion

## 9. Deployment Architecture

### 9.1 Development Environment
```yaml
services:
  backend:
    image: betimes-backend:dev
    ports: ["8000:8000"]
    environment:
      - DEBUG=True
      - DATABASE_URL=postgresql://localhost/betimes_dev
  
  frontend:
    image: betimes-frontend:dev
    ports: ["3000:3000"]
  
  postgres:
    image: postgres:15
    ports: ["5432:5432"]
  
  redis:
    image: redis:7
    ports: ["6379:6379"]
  
  celery:
    image: betimes-backend:dev
    command: celery -A betimes worker -l info
```

### 9.2 Production Deployment
- **Frontend**: Vercel with automatic deployments on main branch
- **Backend**: Render/AWS ECS with Docker containers
- **Database**: AWS RDS PostgreSQL with Multi-AZ
- **Cache**: AWS ElastiCache Redis cluster
- **Storage**: AWS S3 with versioning and lifecycle policies
- **CDN**: CloudFront for global content delivery
- **CI/CD**: GitHub Actions with automated testing

### 9.3 CI/CD Pipeline
1. Code push to GitHub
2. Run linters (flake8, eslint)
3. Run unit tests (pytest, jest)
4. Run integration tests
5. Build Docker images
6. Push to container registry
7. Deploy to staging environment
8. Run smoke tests
9. Deploy to production (blue-green)
10. Run health checks
11. Auto-rollback on failure

## 10. Disaster Recovery

### 10.1 Backup Strategy
- Database: Automated backups every 6 hours
- Files: S3 versioning with 30-day retention
- Backups stored in separate geographic region
- Monthly backup restoration tests

### 10.2 Recovery Objectives
- RPO (Recovery Point Objective): 6 hours
- RTO (Recovery Time Objective): 4 hours

### 10.3 Disaster Recovery Procedures
1. Detect failure through monitoring
2. Assess impact and data loss
3. Restore database from latest backup
4. Restore files from S3 versioning
5. Verify data integrity
6. Redirect traffic to DR environment
7. Monitor system health
8. Document incident and lessons learned

---

## Document Status
**Status**: Complete
**Version**: 1.0
**Created**: 2024
**Last Updated**: 2024

This design document provides a comprehensive, production-ready architecture for the Betimes Enterprise Document Processing Platform, capable of handling 10GB files, millions of documents, and 10,000 concurrent users with world-class performance and reliability.
