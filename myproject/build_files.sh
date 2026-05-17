#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Process static assets using WhiteNoise
python manage.py collectstatic --no-input

# Run database migrations safely against PlanetScale
python manage.py migrate