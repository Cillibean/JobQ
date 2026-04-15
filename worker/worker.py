from celery import Celery
from app.core.config import REDIS_URL

if not REDIS_URL:
    raise Exception("REDIS_URL is not set")

celery_app = Celery("worker", 
                    broker=REDIS_URL, 
                    backend=REDIS_URL,
                    include=["app.tasks.worker_tasks"]
            )

import app.tasks.worker_tasks