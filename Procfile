release: python manage.py migrate --noinput
web: daphne cb_plus.asgi:application --port $PORT --bind 0.0.0.0 -v2
