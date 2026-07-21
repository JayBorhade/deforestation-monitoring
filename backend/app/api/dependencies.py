"""API dependencies."""

from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db


async def get_db_session() -> AsyncSession:
    """Get database session dependency."""
    async for session in get_db():
        yield session
