"""FastAPI application main entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router as api_router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting Call Audio Pipeline API")
    yield
    logger.info("Shutting down Call Audio Pipeline API")


app = FastAPI(
    title="Call Audio Pipeline",
    description="Полноценный воспроизводимый пайплайн потоковой обработки аудио звонков",
    version="0.1.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(api_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "status": "ok",
        "service": "call-audio-pipeline",
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "call-audio-pipeline",
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    return {
        "status": "ready",
        "service": "call-audio-pipeline",
    }
