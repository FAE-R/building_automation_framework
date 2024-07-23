#!/bin/sh
echo "Making init. migrations ... "
python manage.py makemigrations agents admin auth sessions contenttypes --noinput
echo "Migrate ... "
python manage.py migrate --noinput
echo "done"
echo "Creating admin user ... "
python manage.py createadmin
echo "done"
echo "Collectstatics ... "
python manage.py collectstatic --noinput
echo "done"
echo "Run data point server ... "
echo "done"
python manage.py runscript data_points.data_points --continue-on-error &
echo "done"
echo "Make Migrations for logger ... "
python manage.py makemigrations logger --noinput
echo "done"
echo "migrate logger ... "
python manage.py migrate 
echo "done"
echo "Run workers ... "
python manage.py runworker mqtt 
exec "$@"
