import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_monitoring.settings')

app = Celery('currency_monitoring')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'everyday-update-currencies': {
        'task': 'currency.tasks.update_currency_rates',
        'schedule': crontab(hour='0', minute='5', day_of_week='*'),
    },

    'send-telegram-notifications': {
        'task': 'currency.tasks.send_notifications',
        'schedule': crontab(hour='*', minute='*', day_of_week='*'),
    }
}
