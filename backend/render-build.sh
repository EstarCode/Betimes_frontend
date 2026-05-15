#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Betimes Backend Build..."

# Upgrade pip and install build tools
echo "📦 Upgrading pip and build tools..."
python -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input --clear

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input

echo "✅ Build completed successfully!"
