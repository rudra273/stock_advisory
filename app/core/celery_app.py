# # app/celery_app.py

# from celery import Celery
# from celery.schedules import crontab
# from app.core.config import settings

# celery_app = Celery(
#     "worker",
#     broker=settings.CELERY_BROKER_URL,
#     backend=settings.CELERY_RESULT_BACKEND
# )

# celery_app.autodiscover_tasks(['app.tasks'])

# # Configure periodic task
# celery_app.conf.beat_schedule = {
#     'run-every-5-mins': {
#         'task': 'app.tasks.scheduled.periodic_task',
#         'schedule': crontab(minute='*/5'),
#     },
# }

# celery_app.conf.timezone = 'UTC'
