from fastapi.testclient import TestClient

from app.db.models import Job
from app.main import app
from app.services import job_service


def test_health_endpoint_returns_ok():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job_endpoint_persists_job_and_queues_worker(monkeypatch, db_session):
    queued = {}

    def fake_delay(job_id: int):
        queued["job_id"] = job_id

    monkeypatch.setattr(job_service.process_job_task, "delay", fake_delay)

    with TestClient(app) as client:
        response = client.post("/jobs", json={"text": "Hello JobQ"})

    assert response.status_code == 200

    payload = response.json()
    job = db_session.get(Job, payload["job_id"])

    assert payload["status"] == "pending"
    assert job is not None
    assert job.input_data == "Hello JobQ"
    assert job.status == "pending"
    assert queued == {"job_id": job.id}


def test_get_job_endpoint_returns_saved_job(db_session):
    job = Job(input_data="abc", status="completed", result="cba")
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    with TestClient(app) as client:
        response = client.get(f"/jobs/{job.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": job.id,
        "status": "completed",
        "result": "cba",
    }
