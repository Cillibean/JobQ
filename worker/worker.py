from celery import Celery
from app.core.config import REDIS_URL

celery_app = Celery("worker", 
                    broker=REDIS_URL, 
                    backend=REDIS_URL,
                    include=["app.tasks.worker_tasks"]
            )

import app.tasks.worker_tasks