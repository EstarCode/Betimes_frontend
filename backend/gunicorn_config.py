"""
gunicorn_config.py - Production Gunicorn configuration for Render
"""
import os

# --- Binding ---
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# --- Workers ---
# Render free tier has 512MB RAM. 2 workers x 2 threads = safe.
# Formula: (2 x CPU cores) + 1 — but cap at 2 for free tier
workers = 2
threads = 2
worker_class = "gthread"

# --- Timeouts ---
timeout = 120          # PDF processing can take time
graceful_timeout = 30
keepalive = 5

# --- Request limits (auto-restart workers to prevent memory leaks) ---
max_requests = 1000
max_requests_jitter = 50

# --- Logging ---
accesslog = "-"   # stdout
errorlog = "-"    # stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# --- Performance ---
preload_app = True   # Load app before forking workers (saves memory)

# --- Security ---
limit_request_line = 4096
limit_request_fields = 100
