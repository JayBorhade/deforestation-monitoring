from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Any
from shapely.geometry import mapping, Polygon

router = APIRouter()

class PredictRequest(BaseModel):
    # either base64 image or s3_path can be provided; for initial scaffold we accept s3_path
    s3_path: str | None = None
    threshold: float = 0.5

class Detection(BaseModel):
    id: str
    confidence: float
    geometry: Any

class PredictResponse(BaseModel):
    detections: List[Detection]

@router.post("/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest):
    # This is a stubbed implementation returning a mocked polygon detection.
    # Later: wire into backend.ai.infer to run model inference on provided input.
    if not payload.s3_path:
        raise HTTPException(status_code=400, detail="s3_path is required in this scaffold")

    poly = Polygon([(-60.0, -10.0), (-60.0, -10.1), (-59.9, -10.1), (-59.9, -10.0)])
    det = {
        "id": "det-0001",
        "confidence": 0.87,
        "geometry": mapping(poly)
    }

    return {"detections": [det]}
