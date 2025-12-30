from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery('fastapi_client', broker=CELERY_BROKER_URL)
