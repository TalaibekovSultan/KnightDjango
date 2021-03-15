web: gunicorn --bind 0.0.0.0:8000 mysite.wsgi
python manage.py collectstatic --noinput
manage.py makemigrations
manage.py migrate