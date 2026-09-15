"""Database models for call audio pipeline."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.schemas import CallStatus


class CallSession(Base):
    """Model for call sessions."""

    __tablename__ = "call_sessions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    started_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    source_type = Column(String(100), nullable=False)
    sample_rate = Column(Integer, nullable=False, default=16000)
    channels = Column(Integer, nullable=False, default=1)
    consent_given = Column(Boolean, nullable=False, default=True)
    status = Column(String(50), nullable=False, default=CallStatus.INITIATED.value)
    duration_ms = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    transcript_segments = relationship("TranscriptSegment", back_populates="call_session")
    speaker_segments = relationship("SpeakerSegment", back_populates="call_session")
    audio_chunks = relationship("AudioChunk", back_populates="call_session")


class AudioChunk(Base):
    """Model for audio chunks."""

    __tablename__ = "audio_chunks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("call_sessions.id"), nullable=False)
    chunk_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    timestamp_ms = Column(Integer, nullable=False)
    sample_rate = Column(Integer, nullable=False)
    encoding = Column(String(50), nullable=False, default="PCM_16bit")
    duration_ms = Column(Integer, nullable=False)
    has_speech = Column(Boolean, nullable=True)
    vad_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    call_session = relationship("CallSession", back_populates="audio_chunks")


class TranscriptSegment(Base):
    """Model for transcript segments."""

    __tablename__ = "transcript_segments"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("call_sessions.id"), nullable=False)
    start_ms = Column(Integer, nullable=False)
    end_ms = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    speaker = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    is_final = Column(Boolean, nullable=False, default=False)
    language = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    call_session = relationship("CallSession", back_populates="transcript_segments")


class SpeakerSegment(Base):
    """Model for speaker segments."""

    __tablename__ = "speaker_segments"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("call_sessions.id"), nullable=False)
    start_ms = Column(Integer, nullable=False)
    end_ms = Column(Integer, nullable=False)
    speaker_id = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationships
    call_session = relationship("CallSession", back_populates="speaker_segments")


class ConsentRecord(Base):
    """Model for consent records."""

    __tablename__ = "consent_records"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("call_sessions.id"), nullable=False)
    consent_given = Column(Boolean, nullable=False)
    consent_timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    consent_method = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)


class JobStatus(Base):
    """Model for tracking job processing status."""

    __tablename__ = "job_status"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("call_sessions.id"), nullable=False)
    job_type = Column(String(100), nullable=False)  # asr, diarization, postprocessing
    status = Column(String(50), nullable=False)  # pending, processing, completed, failed
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
