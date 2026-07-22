from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import health, predict

app = FastAPI(title="Deforestation Monitoring API")

# CORS (allow local dev origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(predict.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Deforestation Monitoring API - milestone4/phase4 scaffold"}
