from celery import Celery
from ..config import settings


celery_app = Celery(
    "zqt",
    broker=settings.redis_url,
    backend=settings.redis_url,
)


@celery_app.task(name="zqt.ping")
def ping() -> str:
    return "pong"


