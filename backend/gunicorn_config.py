"""
Production Gunicorn Configuration
Optimized for 100,000+ concurrent users
"""
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
backlog = 2048

# Worker processes - optimized for high concurrency
workers = int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'gthread'  # Use threaded workers for better concurrency
threads = 4  # 4 threads per worker
worker_connections = 1000
max_requests = 10000  # Restart workers after 10k requests to prevent memory leaks
max_requests_jitter = 1000
timeout = 120
keepalive = 5

# Graceful timeout
graceful_timeout = 30

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'betimes-api'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Preload app for better performance and memory sharing
preload_app = True

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("🚀 Starting Betimes API Server")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info(f"✅ Server ready with {workers} workers x {threads} threads = {workers * threads} total threads")

def worker_int(worker):
    """Called when a worker receives SIGINT or SIGQUIT."""
    worker.log.info(f"⚠️  Worker {worker.pid} received interrupt signal")

def worker_abort(worker):
    """Called when a worker receives SIGABRT."""
    worker.log.error(f"❌ Worker {worker.pid} aborted")

def post_fork(server, worker):
    """Called after a worker has been forked."""
    server.log.info(f"✅ Worker {worker.pid} spawned")

def pre_fork(server, worker):
    """Called before a worker is forked."""
    pass

def pre_exec(server):
    """Called before a new master process is forked."""
    server.log.info("🔄 Forking new master process")

def on_exit(server):
    """Called just before the master process exits."""
    server.log.info("👋 Server shutting down")
