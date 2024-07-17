#!/bin/sh
echo "Making init. migrations ... "
python manage.py makemigrations --noinput
echo "done"
echo "Migrate ... "
python manage.py migrate --noinput
echo "done"
echo "Creating admin user ... "
python manage.py createadmin
echo "done"
echo "Make Migrations for agents ... "
python manage.py makemigrations agents --noinput
echo "done"
echo "Make migrate django_celery_beat & django_celery_results ... "
python manage.py migrate django_celery_beat
python manage.py migrate django_celery_results
echo "done"
echo "Migrate ... "
python manage.py migrate --noinput
echo "done"
echo "Collectstatics ... "
python manage.py collectstatic --noinput
echo "done"
uvicorn ba_framework.asgi:application --host 0.0.0.0 --port 80 --reload