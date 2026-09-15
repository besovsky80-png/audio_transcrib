"""Pydantic schemas for data validation and serialization."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CallStatus(str, Enum):
    """Status of a call session."""

    INITIATED = "initiated"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ConsentStatus(str, Enum):
    """Consent status for audio processing."""

    GIVEN = "given"
    DENIED = "denied"
    NOT_REQUIRED = "not_required"


# Request Schemas

class StartCallRequest(BaseModel):
    """Request to start a new call session."""

    event: str = Field(default="start_call", description="Event type")
    source_type: str = Field(..., description="Type of audio source")
    sample_rate: int = Field(default=16000, description="Audio sample rate in Hz")
    channels: int = Field(default=1, description="Number of audio channels")
    consent_given: bool = Field(..., description="Whether consent was given")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata")


class AudioChunkResponse(BaseModel):
    """Response confirming audio chunk reception."""

    type: str = Field(default="audio_accepted", description="Response type")
    session_id: UUID = Field(..., description="Session identifier")
    chunk_id: UUID = Field(..., description="Chunk identifier")
    timestamp_ms: int = Field(..., description="Timestamp in milliseconds")


# Response Schemas

class CallSessionBase(BaseModel):
    """Base schema for call session."""

    session_id: UUID
    started_at: datetime
    ended_at: Optional[datetime] = None
    source_type: str
    sample_rate: int
    channels: int
    consent_given: bool
    status: CallStatus
    duration_ms: Optional[int] = None


class CallSessionCreate(BaseModel):
    """Schema for creating a call session."""

    source_type: str
    sample_rate: int = 16000
    channels: int = 1
    consent_given: bool = True


class CallSessionResponse(CallSessionBase):
    """Full response schema for call session."""

    class Config:
        from_attributes = True


class AudioChunkBase(BaseModel):
    """Base schema for audio chunk."""

    session_id: UUID
    chunk_id: UUID
    timestamp_ms: int
    sample_rate: int
    encoding: str = "PCM_16bit"
    duration_ms: int


class TranscriptSegmentBase(BaseModel):
    """Base schema for transcript segment."""

    session_id: UUID
    start_ms: int
    end_ms: int
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    is_final: bool = False
    language: Optional[str] = None


class TranscriptSegmentCreate(TranscriptSegmentBase):
    """Schema for creating a transcript segment."""

    pass


class TranscriptSegmentResponse(TranscriptSegmentBase):
    """Full response schema for transcript segment."""

    segment_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class SpeakerSegmentBase(BaseModel):
    """Base schema for speaker segment."""

    session_id: UUID
    start_ms: int
    end_ms: int
    speaker_id: str
    confidence: Optional[float] = None


class SpeakerSegmentResponse(SpeakerSegmentBase):
    """Full response schema for speaker segment."""

    segment_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class CallResultResponse(BaseModel):
    """Response schema for complete call result."""

    session_id: UUID
    status: CallStatus
    started_at: datetime
    ended_at: Optional[datetime]
    duration_ms: Optional[int]
    consent_given: bool
    segments: list[TranscriptSegmentResponse] = Field(default_factory=list)
    full_text: Optional[str] = None
    language: Optional[str] = None
    audio_url: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str = "call-audio-pipeline"
    database: Optional[str] = None
    redis: Optional[str] = None
    storage: Optional[str] = None


class MetricsResponse(BaseModel):
    """Metrics endpoint response."""

    calls_started_total: int = 0
    calls_completed_total: int = 0
    calls_failed_total: int = 0
    audio_chunks_received_total: int = 0
    asr_segments_total: int = 0
    asr_latency_seconds: Optional[float] = None
    vad_processing_seconds: Optional[float] = None
