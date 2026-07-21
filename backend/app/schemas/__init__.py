"""Pydantic schemas for request/response validation."""

from .deforestation import (
    SatelliteImageCreate,
    SatelliteImageResponse,
    AnalysisResultCreate,
    AnalysisResultResponse,
    AlertCreate,
    AlertResponse,
    AlertUpdate,
    PredictionResponse,
    DeforestationAnalysisRequest,
    HealthCheck,
)

__all__ = [
    "SatelliteImageCreate",
    "SatelliteImageResponse",
    "AnalysisResultCreate",
    "AnalysisResultResponse",
    "AlertCreate",
    "AlertResponse",
    "AlertUpdate",
    "PredictionResponse",
    "DeforestationAnalysisRequest",
    "HealthCheck",
]
