"""API module initialization."""

from fastapi import APIRouter

from app.api import calls, health

router = APIRouter()

# Register endpoints
router.include_router(health.router)
router.include_router(calls.router)
