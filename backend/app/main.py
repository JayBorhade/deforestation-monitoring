"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .api.routes import analysis, alerts, predictions
from .schemas import HealthCheck

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    print(f"🚀 Starting Deforestation Monitoring API v{settings.api_version}")
    print(f"📊 Environment: {settings.environment}")
    print(f"🗄️  Database: {settings.database_url}")
    yield
    # Shutdown
    print("🛑 Shutting down Deforestation Monitoring API")


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
    openapi_url="/api/openapi.json" if settings.debug else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/api/health", response_model=HealthCheck, tags=["Health"])
async def health_check() -> HealthCheck:
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        version=settings.api_version,
        environment=settings.environment,
    )


# Include routers
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(alerts.router, prefix="/api", tags=["Alerts"])
app.include_router(predictions.router, prefix="/api", tags=["Predictions"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return JSONResponse(
        {
            "message": "Deforestation Monitoring API",
            "version": settings.api_version,
            "docs": "/api/docs",
            "health": "/api/health",
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
