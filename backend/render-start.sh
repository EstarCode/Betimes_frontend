#!/usr/bin/env bash
set -o errexit

echo "Starting web process preflight..."

if [ -z "${PORT:-}" ]; then
  echo "ERROR: PORT is not set by platform."
  exit 1
fi

if [ -z "$(printf '%s' "${DATABASE_URL:-}" | tr -d '[:space:]')" ]; then
  echo "ERROR: DATABASE_URL is missing at runtime."
  exit 1
fi

case "$DATABASE_URL" in
  postgres://*|postgresql://*)
    echo "DATABASE_URL runtime format looks valid."
    ;;
  *)
    echo "ERROR: DATABASE_URL runtime value is invalid."
    exit 1
    ;;
esac

echo "Running Django system checks..."
python manage.py check --deploy --fail-level WARNING

echo "Importing WSGI application..."
python -c "import config.wsgi" 

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application -c gunicorn_config.py
