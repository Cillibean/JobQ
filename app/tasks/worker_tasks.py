from worker.worker import celery_app
from app.db.session import get_session_local
from app.db.models import Job
import time

def get_db():
    Session = get_session_local()
    db = Session()
    try:
        yield db
    finally:
        db.close()

@celery_app.task(name="app.tasks.worker_tasks.process_job_task")
def process_job_task(job_id: int):
    Session = get_session_local()
    with Session() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return 
        job.status = "processing"
        db.commit()
        time.sleep(5)
        result = job.input_data[::-1]
        job.status = "completed"
        job.result = result
        db.commit()