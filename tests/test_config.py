"""Tests for configuration loading."""

import os
from unittest.mock import patch


def test_settings_default_values():
    """Test that settings have correct default values."""
    from app.core.config import settings

    assert settings.app_env == "dev"
    assert settings.log_level == "INFO"
    assert settings.api_port == 8000
    assert settings.audio_sample_rate == 16000
    assert settings.audio_chunk_ms == 250
    assert settings.require_consent is True


def test_settings_audio_chunk_samples():
    """Test audio chunk samples calculation."""
    from app.core.config import settings

    # 16000 Hz * 250 ms / 1000 = 4000 samples
    assert settings.audio_chunk_samples == 4000


def test_settings_from_env():
    """Test that settings can be loaded from environment."""
    with patch.dict(os.environ, {
        "APP_ENV": "production",
        "LOG_LEVEL": "WARNING",
        "API_KEY": "test-key-123",
        "REQUIRE_CONSENT": "false",
    }):
        # Need to reload the module to pick up new env vars
        import importlib

        from app.core import config
        importlib.reload(config)

        assert config.settings.app_env == "production"
        assert config.settings.log_level == "WARNING"
        assert config.settings.api_key == "test-key-123"
        assert config.settings.require_consent is False
