web: cd app && gunicorn app.wsgi:application --bind 0.0.0.0:$PORT --workers 2
release: cd app && python manage.py migrate --noinput && python manage.py collectstatic --noinput
