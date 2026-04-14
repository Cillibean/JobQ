from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")
    input_data = Column(Text)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))