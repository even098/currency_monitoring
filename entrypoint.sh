#!/bin/bash
set -e

# Применим миграции перед запуском любого сервиса, кроме Celery Worker
if [ "$1" != "worker" ]; then
    python manage.py migrate
fi

case "$1" in
  web)
    python manage.py runserver 0.0.0.0:8000
    ;;
  bot)
    python bot/main.py
    ;;
  worker)
    celery -A currency_monitoring worker --loglevel=info
    ;;
  beat)
    celery -A currency_monitoring beat --loglevel=info
    ;;
  *)
    exec "$@"
    ;;
esac
