#!/usr/bin/env bash
# exit on error
set -o errexit

echo "================================================"
echo " Betimes Backend Build - Starting"
echo "================================================"

# --- Validate DATABASE_URL early ---
if [ -z "$(printf '%s' "${DATABASE_URL:-}" | tr -d '[:space:]')" ]; then
  echo "ERROR: DATABASE_URL is empty or missing."
  echo "  --> Go to Render dashboard > Environment > Add DATABASE_URL"
  exit 1
fi

case "$DATABASE_URL" in
  postgres://*|postgresql://*)
    echo "[OK] DATABASE_URL format is valid."
    ;;
  *)
    echo "ERROR: DATABASE_URL must start with postgres:// or postgresql://"
    exit 1
    ;;
esac

# --- Upgrade pip only (setuptools/wheel come from requirements.txt) ---
echo "Upgrading pip..."
python -m pip install --upgrade pip

# --- Install all dependencies ---
echo "Installing Python dependencies..."
pip install -r requirements.txt

# --- Verify psycopg2 loads correctly (catches driver issues early) ---
echo "Verifying psycopg2 installation..."
python -c "import psycopg2; print('[OK] psycopg2 version:', psycopg2.__version__)"

# --- Verify Django loads correctly ---
echo "Verifying Django installation..."
python -c "import django; print('[OK] Django version:', django.__version__)"

# --- Collect static files ---
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# --- Run database migrations ---
echo "Running database migrations..."
python manage.py migrate --no-input

echo "================================================"
echo " Build completed successfully!"
echo "================================================"
