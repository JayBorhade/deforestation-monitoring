"""Deforestation monitoring schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SatelliteImageCreate(BaseModel):
    """Schema for creating satellite image records."""

    tile_id: str = Field(..., min_length=1, max_length=100)
    source: str = Field(..., min_length=1, max_length=50)
    acquisition_date: datetime
    cloud_coverage: float = Field(..., ge=0, le=100)
    resolution: int = Field(..., gt=0)
    rgb_path: str
    nir_path: Optional[str] = None
    raw_path: Optional[str] = None
    metadata: dict = Field(default_factory=dict)


class SatelliteImageResponse(BaseModel):
    """Schema for satellite image responses."""

    id: str
    tile_id: str
    source: str
    acquisition_date: datetime
    cloud_coverage: float
    resolution: int
    is_processed: bool
    processing_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalysisResultCreate(BaseModel):
    """Schema for creating analysis results."""

    satellite_image_id: str
    model_version: str
    analysis_type: str
    deforestation_percentage: float = Field(..., ge=0, le=100)
    forest_coverage_percentage: float = Field(..., ge=0, le=100)
    degradation_percentage: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=1)
    deforestation_mask_path: str
    forest_mask_path: Optional[str] = None
    quality_metrics: dict = Field(default_factory=dict)
    is_significant_change: bool = False
    change_magnitude: Optional[float] = None


class AnalysisResultResponse(BaseModel):
    """Schema for analysis result responses."""

    id: str
    satellite_image_id: str
    model_version: str
    analysis_type: str
    deforestation_percentage: float
    forest_coverage_percentage: float
    degradation_percentage: float
    confidence_score: float
    is_significant_change: bool
    change_magnitude: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AlertCreate(BaseModel):
    """Schema for creating alerts."""

    analysis_result_id: str
    severity: str = Field(..., regex="^(low|medium|high|critical)$")
    alert_type: str
    area_hectares: float = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    recommendations: Optional[str] = None
    metadata: dict = Field(default_factory=dict)


class AlertResponse(BaseModel):
    """Schema for alert responses."""

    id: str
    analysis_result_id: str
    severity: str
    alert_type: str
    area_hectares: float
    title: str
    description: str
    status: str
    is_acknowledged: bool
    created_at: datetime
    updated_at: datetime
    acknowledged_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AlertUpdate(BaseModel):
    """Schema for updating alerts."""

    status: Optional[str] = Field(None, regex="^(active|resolved|ignored)$")
    is_acknowledged: Optional[bool] = None
    recommendations: Optional[str] = None


class PredictionResponse(BaseModel):
    """Schema for prediction responses."""

    id: str
    model_version: str
    prediction_date: datetime
    valid_until: datetime
    risk_score: float
    confidence: float
    risk_level: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DeforestationAnalysisRequest(BaseModel):
    """Schema for deforestation analysis requests."""

    satellite_image_id: str
    analysis_type: str = "deforestation"
    model_version: Optional[str] = None


class HealthCheck(BaseModel):
    """Schema for health check responses."""

    status: str
    version: str
    environment: str
