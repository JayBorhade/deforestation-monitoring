from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Any
from app.ai.infer import run_inference

router = APIRouter()

class PredictRequest(BaseModel):
    s3_path: str | None = None
    local_path: str | None = None
    threshold: float = 0.5

class Detection(BaseModel):
    id: str
    confidence: float
    geometry: Any

class PredictResponse(BaseModel):
    detections: List[Detection]

@router.post("/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest):
    input_path = None
    if payload.s3_path:
        input_path = payload.s3_path
    elif payload.local_path:
        input_path = payload.local_path
    else:
        raise HTTPException(status_code=400, detail="s3_path or local_path is required")

    try:
        detections = run_inference(input_path, threshold=payload.threshold)
    except Exception as e:
        # If inference errors, fallback to empty list but surface error in logs
        print("Error during inference:", e)
        detections = []

    return {"detections": detections}
