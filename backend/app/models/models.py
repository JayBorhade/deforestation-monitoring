from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class IngestionRun(Base):
    __tablename__ = "ingestion_runs"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(256), nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Detection(Base):
    __tablename__ = "detections"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("ingestion_runs.id"), nullable=True)
    geometry = Column(JSON, nullable=False)  # GeoJSON
    confidence = Column(Float, nullable=False)
    properties = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    run = relationship("IngestionRun", backref="detections")
