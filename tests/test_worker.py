from app.db.models import Job
from app.tasks import worker_tasks


def test_process_job_task_updates_job_result(monkeypatch, db_session):
    job = Job(input_data="abcdef", status="pending")
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    monkeypatch.setattr(worker_tasks.time, "sleep", lambda _: None)

    worker_tasks.process_job_task.run(job.id)

    db_session.expire_all()
    processed_job = db_session.get(Job, job.id)

    assert processed_job is not None
    assert processed_job.status == "completed"
    assert processed_job.result == "fedcba"
