#!/bin/bash
if [ "$RAILWAY_SERVICE_NAME" = "web" ]; then
  python manage.py migrate
  python manage.py collectstatic --noinput
  python manage.py runserver 0.0.0.0:8000
elif [ "$RAILWAY_SERVICE_NAME" = "celery" ]; then
  celery -A currency_monitoring worker --loglevel=info &
  celery -A currency_monitoring beat --loglevel=info
elif [ "$RAILWAY_SERVICE_NAME" = "web+bot" ]; then
  # запускаем web и bot параллельно
  python manage.py runserver 0.0.0.0:8000 &
  python bot/main.py
fi
