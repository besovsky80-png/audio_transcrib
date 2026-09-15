"""Calls API endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import CallSession
from app.db.session import get_db
from app.schemas import CallResultResponse, CallSessionResponse

router = APIRouter(prefix="/calls", tags=["calls"])


@router.get("", response_model=List[CallSessionResponse])
async def list_calls(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get list of all call sessions."""
    calls = db.query(CallSession).offset(skip).limit(limit).all()
    return calls


@router.get("/{session_id}", response_model=CallSessionResponse)
async def get_call(
    session_id: UUID,
    db: Session = Depends(get_db),
):
    """Get details of a specific call session."""
    call = db.query(CallSession).filter(CallSession.id == session_id).first()
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call session {session_id} not found",
        )
    return call


@router.get("/{session_id}/transcript", response_model=CallResultResponse)
async def get_transcript(
    session_id: UUID,
    db: Session = Depends(get_db),
):
    """Get transcript for a specific call session."""
    call = db.query(CallSession).filter(CallSession.id == session_id).first()
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call session {session_id} not found",
        )

    # Build response with transcript segments
    from app.schemas import TranscriptSegmentResponse

    segments = []
    for segment in call.transcript_segments:
        segments.append(TranscriptSegmentResponse(
            segment_id=segment.id,
            session_id=segment.session_id,
            start_ms=segment.start_ms,
            end_ms=segment.end_ms,
            text=segment.text,
            speaker=segment.speaker,
            confidence=segment.confidence,
            is_final=segment.is_final,
            language=segment.language,
            created_at=segment.created_at,
        ))

    full_text = " ".join([s.text for s in sorted(segments, key=lambda x: x.start_ms)])

    return CallResultResponse(
        session_id=call.id,
        status=call.status,
        started_at=call.started_at,
        ended_at=call.ended_at,
        duration_ms=call.duration_ms,
        consent_given=call.consent_given,
        segments=segments,
        full_text=full_text,
        language=segments[0].language if segments else None,
    )
