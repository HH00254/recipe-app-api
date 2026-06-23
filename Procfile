web: gunicorn app.wsgi:application --chdir app --bind 0.0.0.0:$PORT --workers 2
release: bash -c "cd app && python manage.py migrate --noinput && python manage.py collectstatic --noinput"