#!/usr/bin/env bash
# exit on error
set -o errexit

echo "================================================"
echo " Betimes Backend - Starting Web Process"
echo "================================================"

# --- Validate PORT ---
if [ -z "${PORT:-}" ]; then
  echo "ERROR: PORT is not set by platform."
  exit 1
fi
echo "[OK] PORT = $PORT"

# --- Validate DATABASE_URL ---
if [ -z "$(printf '%s' "${DATABASE_URL:-}" | tr -d '[:space:]')" ]; then
  echo "ERROR: DATABASE_URL is missing at runtime."
  exit 1
fi

case "$DATABASE_URL" in
  postgres://*|postgresql://*)
    echo "[OK] DATABASE_URL format is valid."
    ;;
  *)
    echo "ERROR: DATABASE_URL runtime value is invalid."
    exit 1
    ;;
esac

# --- Run Django basic checks (NOT --deploy to avoid WARNING-level failures) ---
# --deploy check is too strict for Render free tier (HTTPS/HSTS warnings will kill startup)
echo "Running Django system checks..."
python manage.py check --fail-level ERROR

# --- Verify WSGI app imports correctly ---
echo "Importing WSGI application..."
python -c "import config.wsgi; print('[OK] WSGI application loaded successfully')"

# --- Start Gunicorn with production settings ---
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 2 \
  --threads 2 \
  --timeout 120 \
  --max-requests 1000 \
  --max-requests-jitter 50 \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  --preload
