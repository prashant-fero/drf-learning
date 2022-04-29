from django.utils.crypto import get_random_string
from celery.utils.log import get_task_logger
from celery import shared_task
import time

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    for i in range(10):
        logger.info(f"print record {i}")
        time.sleep(1)
    return x + y
