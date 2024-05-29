from celery import Celery
from common.settings import settings

celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URI,
    backend=settings.CELERY_RESULT_BACKEND,
)
celery.autodiscover_tasks(["app.auth", "app.images"])
