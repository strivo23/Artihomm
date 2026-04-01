#!/bin/bash
set -e

echo "--- Installing dependencies ---"
pip3 install -r requirements.txt

echo "--- Collecting static files ---"
python3 manage.py collectstatic --no-input

echo "--- Checking migrations (must be committed) ---"
python3 manage.py makemigrations --check --dry-run

echo "--- Running migrations ---"
python3 manage.py migrate --noinput

echo "--- Creating superuser ---"
python3 manage.py create_superuser

echo "--- Seeding products ---"
python3 manage.py seed_products || echo "Warning: Product seeding failed, but continuing..."

echo "--- Build complete ---"
