#!/bin/sh

python manage.py wait_for_db
python manage.py makemigrations --noinput
python manage.py migrate

if [ "$ENVIRONMENT" = "development" ]; then
    echo 'Running Django development server...'
    python manage.py runserver 0.0.0.0:8000
elif [ "$ENVIRONMENT" = "staging" ]; then
    echo 'Running Django staging server...'
    python manage.py collectstatic --noinput
    exec gunicorn base.wsgi:application --bind 0.0.0.0:8000
elif [ "$ENVIRONMENT" = "production" ]; then
    echo 'Running Django production server...'
    python manage.py collectstatic --noinput
    exec gunicorn --workers $GUNICORN_WORKERS --worker-class gthread --threads $GUNICORN_THREADS base.wsgi:application --bind 0.0.0.0:8000
else
    echo "Unknown environment: '$ENVIRONMENT'. Please set ENVIRONMENT to 'development', 'staging', or 'production'."
    exit 1
fi
