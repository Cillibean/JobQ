from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Enum as EnumSQL
from enum import Enum
from session import Base
from datetime import datetime, timezone

class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"

class Job(Base):
    __tablename__ = "jobs"

    id = Column("id", Integer, primary_key=True, index=True)
    status = Column("status", EnumSQL(Status, create_constraint=True), default=Status.PENDING, index=True)
    input_data = Column("input_data", String, index=True)
    result = Column("result", String, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)