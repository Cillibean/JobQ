from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.routes import router
from app.db.models import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}