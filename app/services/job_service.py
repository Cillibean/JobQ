from app.db.session import get_session_local
from app.db.models import Job
from app.tasks.worker_tasks import process_job_task

def get_db():
    Session = get_session_local()
    db = Session()
    try:
        yield db
    finally:
        db.close()

def create_job(text: str):
    job = None
    Session = get_session_local()
    with Session() as db:
        job = Job(input_data=text, status="pending")
        db.add(job)
        db.commit()
        db.refresh(job)
        process_job_task.delay(job.id)
        return {"job_id": job.id, "status": job.status}
    return {"error": "Failed to create job"}

def get_job(job_id: int):
    job = None
    Session = get_session_local()
    with Session() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return {"error": "Job not found"}
        else:
            return {"id": job.id, 
                    "status": job.status,
                    "result": job.result
            }
    return {"error": "Failed to retrieve job"}