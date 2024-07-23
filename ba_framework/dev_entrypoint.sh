#!/bin/sh
echo "Making init. migrations ... "
python manage.py makemigrations agents admin auth sessions contenttypes --noinput
echo "done"
echo "Migrate ... "
python manage.py migrate --noinput
echo "done"
echo "Creating admin user ... "
python manage.py createadmin
echo "done"
# echo "Make Migrations for logger ... "
# python manage.py makemigrations logger --noinput
# echo "done"
#echo "migrate logger ... "
# python manage.py migrate 
# echo "done"
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
celery -A ba_framework worker -l info
celery -A ba_framework beat -l info