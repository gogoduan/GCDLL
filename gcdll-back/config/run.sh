python3 manage.py makemigrations
python3 manage.py migrate
uwsgi --exit
service nginx stop
service nginx start
uwsgi --ini uwsgi.ini --env DJANGO_SETTINGS_MODULE=PhotoGallery.settings
