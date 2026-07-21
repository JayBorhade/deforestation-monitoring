"""Deforestation monitoring database models."""

from datetime import datetime
from uuid import uuid4

from geoalchemy2 import Geometry
from sqlalchemy import (
    JSON,
    Float,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class SatelliteImage(Base):
    """Satellite imagery data model."""

    __tablename__ = "satellite_images"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tile_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    source: Mapped[str] = mapped_column(String(50))  # Sentinel-2, Landsat, etc.
    acquisition_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    geometry: Mapped[str] = mapped_column(Geometry("POLYGON", srid=4326))
    
    # File paths
    rgb_path: Mapped[str] = mapped_column(String(500))
    nir_path: Mapped[str] = mapped_column(String(500), nullable=True)
    raw_path: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Metadata
    cloud_coverage: Mapped[float] = mapped_column(Float)
    resolution: Mapped[int] = mapped_column(Integer)  # meters
    metadata: Mapped[dict] = mapped_column(JSON)
    
    # Processing
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    processing_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    analysis_results: Mapped[list["AnalysisResult"]] = relationship(
        "AnalysisResult", back_populates="satellite_image", cascade="all, delete-orphan"
    )


class AnalysisResult(Base):
    """Deforestation analysis results."""

    __tablename__ = "analysis_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    satellite_image_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("satellite_images.id"), index=True
    )
    
    # Analysis metadata
    model_version: Mapped[str] = mapped_column(String(50))
    analysis_type: Mapped[str] = mapped_column(String(50))  # deforestation, forest_cover, etc.
    
    # Results
    deforestation_percentage: Mapped[float] = mapped_column(Float)
    forest_coverage_percentage: Mapped[float] = mapped_column(Float)
    degradation_percentage: Mapped[float] = mapped_column(Float)
    
    # Confidence and quality metrics
    confidence_score: Mapped[float] = mapped_column(Float)  # 0-1
    quality_metrics: Mapped[dict] = mapped_column(JSON)
    
    # Masks and predictions
    deforestation_mask_path: Mapped[str] = mapped_column(String(500))
    forest_mask_path: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Change detection
    is_significant_change: Mapped[bool] = mapped_column(Boolean, default=False)
    change_magnitude: Mapped[float] = mapped_column(Float, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    satellite_image: Mapped["SatelliteImage"] = relationship(
        "SatelliteImage", back_populates="analysis_results"
    )
    alerts: Mapped[list["Alert"]] = relationship(
        "Alert", back_populates="analysis_result", cascade="all, delete-orphan"
    )


class Alert(Base):
    """Deforestation alerts."""

    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    analysis_result_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("analysis_results.id"), index=True
    )
    
    # Alert details
    severity: Mapped[str] = mapped_column(String(20))  # low, medium, high, critical
    alert_type: Mapped[str] = mapped_column(String(50))  # deforestation, degradation, etc.
    
    # Location
    geometry: Mapped[str] = mapped_column(Geometry("POLYGON", srid=4326))
    area_hectares: Mapped[float] = mapped_column(Float)
    
    # Alert content
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    recommendations: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, resolved, ignored
    is_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(JSON)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    acknowledged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    analysis_result: Mapped["AnalysisResult"] = relationship(
        "AnalysisResult", back_populates="alerts"
    )


class Prediction(Base):
    """Deforestation hotspot predictions."""

    __tablename__ = "predictions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    
    # Prediction details
    model_version: Mapped[str] = mapped_column(String(50))
    prediction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    # Prediction data
    hotspot_geometry: Mapped[str] = mapped_column(Geometry("POLYGON", srid=4326))
    risk_score: Mapped[float] = mapped_column(Float)  # 0-1
    confidence: Mapped[float] = mapped_column(Float)  # 0-1
    
    # Risk classification
    risk_level: Mapped[str] = mapped_column(String(20))  # low, medium, high, critical
    
    # Prediction features
    historical_deforestation_rate: Mapped[float] = mapped_column(Float, nullable=True)
    proximity_to_roads: Mapped[float] = mapped_column(Float, nullable=True)
    proximity_to_settlements: Mapped[float] = mapped_column(Float, nullable=True)
    slope: Mapped[float] = mapped_column(Float, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(JSON)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
