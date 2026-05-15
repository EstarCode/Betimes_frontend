#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install build tools
pip install --upgrade pip
pip install wheel setuptools

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
