<<<<<<< HEAD
web: gunicorn ekthal.wsgi:application
=======
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ekthal.wsgi:application --bind 0.0.0.0:$PORT
>>>>>>> b4c8a48ade4829f0e06836e4cb3da3911c17ed0a
