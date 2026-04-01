#!/bin/bash
set -e

echo "--- Installing dependencies ---"
pip install -r requirements.txt

echo "--- Collecting static files ---"
python manage.py collectstatic --no-input

echo "--- Running migrations ---"
python manage.py migrate

echo "--- Seeding products ---"
python manage.py seed_products || echo "Warning: Product seeding failed, but continuing..."

echo "--- Build complete ---"
