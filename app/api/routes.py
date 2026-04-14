from fastapi import APIRouter
from app.services.job_service import create_job, get_job

router = APIRouter()

@router.post("/jobs")
def create_job_endpoint(data: dict):
    return create_job(data["text"])

@router.get("/jobs/{job_id}")
def get_job_endpoint(job_id: int):
    return get_job(job_id)