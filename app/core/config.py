"""Core configuration and settings for the application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_env: str = "dev"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/calls"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Storage (MinIO)
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minio"
    minio_secret_key: str = "minio123"
    minio_bucket: str = "calls"
    minio_secure: bool = False

    # Audio settings
    audio_sample_rate: int = 16000
    audio_chunk_ms: int = 250

    # ASR settings
    asr_model: str = "tiny"
    asr_device: str = "cpu"

    # VAD settings
    vad_threshold: float = 0.5

    # Diarization
    enable_diarization: bool = False

    # Security
    api_key: str = "changeme"
    require_consent: bool = True

    # Retention
    retention_days: int = 30

    @property
    def audio_chunk_samples(self) -> int:
        """Calculate number of samples per chunk."""
        return int(self.audio_sample_rate * self.audio_chunk_ms / 1000)


settings = Settings()
