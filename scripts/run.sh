#!/bin/sh

# poetry run python manage.py makemigrations
# poetry run python manage.py migrate 
# poetry run python manage.py collectstatic --noinput --settings="core.settings.prod"
# poetry run gunicorn --workers=2 --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE='core.settings.prod' core.wsgi:application
poetry run python manage.py runserver 0.0.0.0:8000