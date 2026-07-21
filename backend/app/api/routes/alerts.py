"""Alert management endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...database import get_db
from ...models import Alert, AnalysisResult
from ...schemas import AlertCreate, AlertResponse, AlertUpdate

router = APIRouter()


@router.post("/alerts", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert: AlertCreate,
    db: AsyncSession = Depends(get_db),
) -> AlertResponse:
    """Create a new alert."""
    # Verify analysis result exists
    result = await db.execute(
        select(AnalysisResult).where(AnalysisResult.id == alert.analysis_result_id)
    )
    if not result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis result with id '{alert.analysis_result_id}' not found",
        )

    db_alert = Alert(**alert.model_dump())
    db.add(db_alert)
    await db.commit()
    await db.refresh(db_alert)
    return AlertResponse.model_validate(db_alert)


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: str,
    db: AsyncSession = Depends(get_db),
) -> AlertResponse:
    """Get alert by ID."""
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    db_alert = result.scalars().first()
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id '{alert_id}' not found",
        )
    return AlertResponse.model_validate(db_alert)


@router.get("/alerts", response_model=List[AlertResponse])
async def list_alerts(
    severity: str = None,
    status_filter: str = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> List[AlertResponse]:
    """List alerts with optional filtering."""
    query = select(Alert)
    
    if severity:
        query = query.where(Alert.severity == severity)
    if status_filter:
        query = query.where(Alert.status == status_filter)
    
    result = await db.execute(
        query.offset(skip).limit(limit).order_by(Alert.created_at.desc())
    )
    alerts = result.scalars().all()
    return [AlertResponse.model_validate(alert) for alert in alerts]


@router.patch("/alerts/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: str,
    alert_update: AlertUpdate,
    db: AsyncSession = Depends(get_db),
) -> AlertResponse:
    """Update an alert."""
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    db_alert = result.scalars().first()
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id '{alert_id}' not found",
        )

    update_data = alert_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    await db.commit()
    await db.refresh(db_alert)
    return AlertResponse.model_validate(db_alert)


@router.get("/alerts/stats/summary")
async def get_alerts_summary(db: AsyncSession = Depends(get_db)):
    """Get alerts summary statistics."""
    result = await db.execute(select(Alert))
    alerts = result.scalars().all()
    
    summary = {
        "total": len(alerts),
        "by_severity": {},
        "by_status": {},
        "acknowledged": sum(1 for a in alerts if a.is_acknowledged),
    }
    
    for severity in ["low", "medium", "high", "critical"]:
        summary["by_severity"][severity] = sum(1 for a in alerts if a.severity == severity)
    
    for status_val in ["active", "resolved", "ignored"]:
        summary["by_status"][status_val] = sum(1 for a in alerts if a.status == status_val)
    
    return summary
