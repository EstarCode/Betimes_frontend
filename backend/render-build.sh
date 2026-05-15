#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Betimes Backend Build..."

# Upgrade pip and install build tools
echo "📦 Upgrading pip and build tools..."
pip install --upgrade pip
pip install wheel setuptools

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run production readiness checks
echo "🔍 Running production readiness checks..."
python production-checklist.py || echo "⚠️  Some checks failed, but continuing..."

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

echo "✅ Build completed successfully!"
