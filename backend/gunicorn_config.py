"""
Production Gunicorn Configuration
Optimized for managed deployment stability on Render.
"""
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'gthread'
threads = 2
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 5
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

# Security limits
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Safer startup on PaaS: avoid preload import-time crash bringing down master
preload_app = False


def on_starting(server):
    server.log.info('Starting Betimes API Server')


def when_ready(server):
    server.log.info(
        f'Server ready with {workers} workers x {threads} threads = {workers * threads} total threads'
    )


def worker_int(worker):
    worker.log.info(f'Worker {worker.pid} received interrupt signal')


def worker_abort(worker):
    worker.log.error(f'Worker {worker.pid} aborted')


def post_fork(server, worker):
    server.log.info(f'Worker {worker.pid} spawned')


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info('Forking new master process')


def on_exit(server):
    server.log.info('Server shutting down')
