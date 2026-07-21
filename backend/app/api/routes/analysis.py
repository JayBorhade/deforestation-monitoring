"""Analysis endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...database import get_db
from ...models import AnalysisResult, SatelliteImage
from ...schemas import (
    AnalysisResultCreate,
    AnalysisResultResponse,
    SatelliteImageCreate,
    SatelliteImageResponse,
)

router = APIRouter()


@router.post("/satellite-images", response_model=SatelliteImageResponse, status_code=status.HTTP_201_CREATED)
async def create_satellite_image(
    satellite_image: SatelliteImageCreate,
    db: AsyncSession = Depends(get_db),
) -> SatelliteImageResponse:
    """Create a new satellite image record."""
    # Check if image already exists
    result = await db.execute(
        select(SatelliteImage).where(SatelliteImage.tile_id == satellite_image.tile_id)
    )
    existing = result.scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Satellite image with tile_id '{satellite_image.tile_id}' already exists",
        )

    db_image = SatelliteImage(**satellite_image.model_dump())
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return SatelliteImageResponse.model_validate(db_image)


@router.get("/satellite-images/{image_id}", response_model=SatelliteImageResponse)
async def get_satellite_image(
    image_id: str,
    db: AsyncSession = Depends(get_db),
) -> SatelliteImageResponse:
    """Get satellite image by ID."""
    result = await db.execute(select(SatelliteImage).where(SatelliteImage.id == image_id))
    db_image = result.scalars().first()
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Satellite image with id '{image_id}' not found",
        )
    return SatelliteImageResponse.model_validate(db_image)


@router.get("/satellite-images", response_model=List[SatelliteImageResponse])
async def list_satellite_images(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> List[SatelliteImageResponse]:
    """List all satellite images."""
    result = await db.execute(
        select(SatelliteImage).offset(skip).limit(limit).order_by(SatelliteImage.created_at.desc())
    )
    images = result.scalars().all()
    return [SatelliteImageResponse.model_validate(img) for img in images]


@router.post(
    "/analysis-results", response_model=AnalysisResultResponse, status_code=status.HTTP_201_CREATED
)
async def create_analysis_result(
    analysis: AnalysisResultCreate,
    db: AsyncSession = Depends(get_db),
) -> AnalysisResultResponse:
    """Create a new analysis result."""
    # Verify satellite image exists
    result = await db.execute(
        select(SatelliteImage).where(SatelliteImage.id == analysis.satellite_image_id)
    )
    if not result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Satellite image with id '{analysis.satellite_image_id}' not found",
        )

    db_analysis = AnalysisResult(**analysis.model_dump())
    db.add(db_analysis)
    await db.commit()
    await db.refresh(db_analysis)
    return AnalysisResultResponse.model_validate(db_analysis)


@router.get("/analysis-results/{result_id}", response_model=AnalysisResultResponse)
async def get_analysis_result(
    result_id: str,
    db: AsyncSession = Depends(get_db),
) -> AnalysisResultResponse:
    """Get analysis result by ID."""
    result = await db.execute(select(AnalysisResult).where(AnalysisResult.id == result_id))
    db_result = result.scalars().first()
    if not db_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis result with id '{result_id}' not found",
        )
    return AnalysisResultResponse.model_validate(db_result)


@router.get("/analysis-results", response_model=List[AnalysisResultResponse])
async def list_analysis_results(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> List[AnalysisResultResponse]:
    """List all analysis results."""
    result = await db.execute(
        select(AnalysisResult).offset(skip).limit(limit).order_by(AnalysisResult.created_at.desc())
    )
    results = result.scalars().all()
    return [AnalysisResultResponse.model_validate(r) for r in results]
