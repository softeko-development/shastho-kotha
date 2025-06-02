import os
from datetime import timedelta

from celery import Celery
from time import sleep
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telmed.settings')

app = Celery('attendance')
app.conf.broker_connection_retry_on_startup = True
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'update-doctor-status-every-minute': {
#         'task': 'conference.tasks.update_doctor_status',
#         'schedule': crontab(minute='*/1'),  # Run every minute
#     },
# }

app.conf.beat_schedule = {
    'update-doctor-status-every-20-seconds': {
        'task': 'conference.tasks.update_doctor_status',
        'schedule': timedelta(seconds=20),  # Run every 20 seconds
    },
}