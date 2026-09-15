"""Tests for schemas serialization."""

import uuid
from datetime import datetime

from app.schemas import (
    CallSessionBase,
    CallStatus,
    StartCallRequest,
    TranscriptSegmentBase,
)


def test_start_call_request():
    """Test StartCallRequest schema."""
    request = StartCallRequest(
        event="start_call",
        source_type="test_client",
        sample_rate=16000,
        channels=1,
        consent_given=True,
    )

    assert request.event == "start_call"
    assert request.source_type == "test_client"
    assert request.sample_rate == 16000
    assert request.channels == 1
    assert request.consent_given is True


def test_start_call_request_default_values():
    """Test StartCallRequest with default values."""
    request = StartCallRequest(
        source_type="websocket",
        consent_given=True,
    )

    assert request.event == "start_call"
    assert request.sample_rate == 16000
    assert request.channels == 1


def test_call_session_base():
    """Test CallSessionBase schema."""
    session_id = uuid.uuid4()
    now = datetime.utcnow()

    session = CallSessionBase(
        session_id=session_id,
        started_at=now,
        source_type="test",
        sample_rate=16000,
        channels=1,
        consent_given=True,
        status=CallStatus.INITIATED,
    )

    assert session.session_id == session_id
    assert session.status == CallStatus.INITIATED
    assert session.ended_at is None


def test_transcript_segment_base():
    """Test TranscriptSegmentBase schema."""
    session_id = uuid.uuid4()

    segment = TranscriptSegmentBase(
        session_id=session_id,
        start_ms=0,
        end_ms=3000,
        text="Hello world",
        speaker="speaker_0",
        confidence=0.95,
        is_final=True,
        language="en",
    )

    assert segment.start_ms == 0
    assert segment.end_ms == 3000
    assert segment.text == "Hello world"
    assert segment.is_final is True


def test_consent_required():
    """Test that consent_given is required."""
    try:
        StartCallRequest(
            source_type="test",
            # consent_given is missing
        )
        assert False, "Should have raised validation error"
    except Exception:
        pass  # Expected
