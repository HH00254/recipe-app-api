#!/bin/sh
set -e

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Seeding demo data ==="
python manage.py seed_data && echo "Seed complete." || echo "Seed skipped (data may already exist)."

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput || echo "collectstatic warning — continuing."

echo "=== Starting gunicorn ==="
exec gunicorn app.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers 2 \
    --log-level info
