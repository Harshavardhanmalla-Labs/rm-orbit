import os
from datetime import timedelta

class Settings:
    # App
    APP_NAME = "Research Backend"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://research:research@localhost:5432/research"
    )
    DB_ECHO = DEBUG
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
    DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    DB_POOL_TIMEOUT = 10

    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_SOCKET_TIMEOUT = 5
    REDIS_SOCKET_CONNECT_TIMEOUT = 5
    REDIS_RETRY_ON_TIMEOUT = True

    # Celery
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_TRACK_STARTED = True

    # CRITICAL FIX: Task timeout must fit within lock safety window
    # Lock acquired at T=0, TTL=600s
    # Lock extended at T=240, new TTL=600s (expires at T=840)
    # Task must complete before T=840 to avoid lock expiration
    # Soft timeout at 300s = 5 minutes (safe margin)
    # Hard timeout at 310s = 5m 10s (abort point)
    CELERY_TASK_SOFT_TIME_LIMIT = 300    # 5 minutes (soft timeout)
    CELERY_TASK_TIME_LIMIT = 310         # 5m 10s (hard timeout)

    CELERY_WORKER_PREFETCH_MULTIPLIER = 4
    CELERY_WORKER_MAX_TASKS_PER_CHILD = 100

    # Timeouts (seconds)
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
    CROSSREF_TIMEOUT = int(os.getenv("CROSSREF_TIMEOUT", "10"))
    OPENALES_TIMEOUT = int(os.getenv("OPENALES_TIMEOUT", "10"))
    CLAUDE_TIMEOUT = int(os.getenv("CLAUDE_TIMEOUT", "60"))

    # Rate limits (req/sec)
    CROSSREF_RATE_LIMIT = int(os.getenv("CROSSREF_RATE_LIMIT", "40"))
    OPENALES_RATE_LIMIT = int(os.getenv("OPENALES_RATE_LIMIT", "50"))
    CLAUDE_RATE_LIMIT = int(os.getenv("CLAUDE_RATE_LIMIT", "1"))

    # Circuit breaker
    CIRCUIT_BREAKER_FAILURE_THRESHOLD = 0.3  # 30%
    CIRCUIT_BREAKER_RECOVERY_TIMEOUT = 120   # 120 seconds

    # Backpressure
    QUEUE_DEPTH_HIGH = int(os.getenv("QUEUE_DEPTH_HIGH", "200"))
    QUEUE_DEPTH_LOW = int(os.getenv("QUEUE_DEPTH_LOW", "50"))
    ERROR_RATE_PAUSE_THRESHOLD = 0.05  # 5%
    ERROR_RATE_RESUME_THRESHOLD = 0.01  # 1%

    # Worker scaling
    MIN_WORKERS = 2
    MAX_WORKERS = 16

    # Auth (placeholder)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")

    # Feature flags
    ENABLE_AUTO_SCALING = os.getenv("ENABLE_AUTO_SCALING", "true").lower() == "true"
    ENABLE_CIRCUIT_BREAKERS = os.getenv("ENABLE_CIRCUIT_BREAKERS", "true").lower() == "true"
    ENABLE_CONTROL_LOOP = os.getenv("ENABLE_CONTROL_LOOP", "true").lower() == "true"

settings = Settings()
