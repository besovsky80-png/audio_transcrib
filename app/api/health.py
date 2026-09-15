"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def get_health(db: Session = Depends(get_db)):
    """Get health status of the service and dependencies."""
    health_status = {
        "status": "ok",
        "service": "call-audio-pipeline",
    }

    # Check database
    try:
        db.execute("SELECT 1")
        health_status["database"] = "ok"
    except Exception:
        health_status["database"] = "error"
        health_status["status"] = "degraded"

    # Check Redis
    try:
        import redis

        from app.core.config import settings
        redis_client = redis.from_url(settings.redis_url)
        redis_client.ping()
        health_status["redis"] = "ok"
    except Exception:
        health_status["redis"] = "error"
        health_status["status"] = "degraded"

    # Check storage
    try:
        from minio import Minio

        from app.core.config import settings
        minio_client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        minio_client.bucket_exists(settings.minio_bucket)
        health_status["storage"] = "ok"
    except Exception:
        health_status["storage"] = "error"
        health_status["status"] = "degraded"

    return health_status
