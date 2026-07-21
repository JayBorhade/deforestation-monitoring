"""Prediction endpoints."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...database import get_db
from ...models import Prediction
from ...schemas import PredictionResponse

router = APIRouter()


@router.get("/predictions", response_model=List[PredictionResponse])
async def list_predictions(
    risk_level: str = None,
    is_active: bool = True,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> List[PredictionResponse]:
    """List predictions with optional filtering."""
    query = select(Prediction)
    
    if risk_level:
        query = query.where(Prediction.risk_level == risk_level)
    if is_active is not None:
        query = query.where(Prediction.is_active == is_active)
    
    result = await db.execute(
        query.offset(skip).limit(limit).order_by(Prediction.risk_score.desc())
    )
    predictions = result.scalars().all()
    return [PredictionResponse.model_validate(p) for p in predictions]


@router.get("/predictions/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(
    prediction_id: str,
    db: AsyncSession = Depends(get_db),
) -> PredictionResponse:
    """Get prediction by ID."""
    result = await db.execute(select(Prediction).where(Prediction.id == prediction_id))
    prediction = result.scalars().first()
    if not prediction:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction with id '{prediction_id}' not found",
        )
    return PredictionResponse.model_validate(prediction)


@router.get("/predictions/stats/risk-distribution")
async def get_risk_distribution(db: AsyncSession = Depends(get_db)):
    """Get risk distribution statistics."""
    result = await db.execute(select(Prediction).where(Prediction.is_active == True))
    predictions = result.scalars().all()
    
    distribution = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0,
        "total": len(predictions),
        "average_risk_score": 0,
    }
    
    for pred in predictions:
        distribution[pred.risk_level] += 1
    
    if predictions:
        distribution["average_risk_score"] = sum(p.risk_score for p in predictions) / len(predictions)
    
    return distribution
