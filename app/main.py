from fastapi import FastAPI
from app.api.routes import router
from app.db.models import Base
from app.db.session import engine

# Create the FastAPI application

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}