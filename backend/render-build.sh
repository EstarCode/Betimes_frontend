#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting Betimes Backend Build..."

# Validate DATABASE_URL early to avoid opaque parser failures later.
if [ -z "$(printf '%s' "$DATABASE_URL" | tr -d '[:space:]')" ]; then
  echo "ERROR: DATABASE_URL is empty or missing. Set it from the PostgreSQL connection string."
  exit 1
fi

case "$DATABASE_URL" in
  postgres://*|postgresql://*)
    echo "DATABASE_URL format looks valid."
    ;;
  *)
    echo "ERROR: DATABASE_URL must start with postgres:// or postgresql://"
    exit 1
    ;;
esac

# Upgrade pip and install build tools
echo "Upgrading pip and build tools..."
python -m pip install --upgrade pip setuptools wheel
python -m pip install "setuptools<81"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --no-input

echo "Build completed successfully."
