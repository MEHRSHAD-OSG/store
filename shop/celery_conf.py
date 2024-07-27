from celery import Celery
from datetime import timedelta
import os

# specified you're project setting
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
# instance
celery_app = Celery('shop',broker='amqp://')
# search in myapp and run task.py file
celery_app.autodiscover_tasks()

# connect broker
celery_app.conf.broker_url = 'amqp://'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
# witch type of data want to use
celery_app.conf.accept_content = ['json', 'pickle']
# time for doing 1 task
celery_app.conf.result_expires = timedelta(days=1)
# waiting user for doing tasks or no = False
celery_app.conf.task_always_eager = False
# how many tasks doing at the same time
celery_app.conf.worker_prefetch_multiplier = 4