from celery import Celery
from celery.schedules import schedule
from kombu import Queue, Exchange
from app.config import settings
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(__name__)

# Load configuration from settings
celery_app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,

    # Serialization
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
    accept_content=settings.CELERY_ACCEPT_CONTENT,

    # Task tracking
    task_track_started=settings.CELERY_TASK_TRACK_STARTED,

    # CRITICAL FIX: Task timeout configured from settings
    # Soft timeout: 300s (5 min) → logs warning, allows graceful shutdown
    # Hard timeout: 310s (5m 10s) → forcefully kills task
    # Lock safety: extended at T=240, expires at T=840
    # Task must complete before T=840 → 300s soft limit is safe
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,  # 300s
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,             # 310s

    # Worker settings
    worker_prefetch_multiplier=settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    worker_max_tasks_per_child=settings.CELERY_WORKER_MAX_TASKS_PER_CHILD,

    # Result backend
    result_expires=3600,  # 1 hour
    result_backend_transport_options={
        "socket_connect_timeout": 5,
        "socket_timeout": 5,
        "retry_on_timeout": True,
    },

    # Task routes
    task_routes={
        'app.tasks.workflow.*': {'queue': 'workflows'},
        'app.tasks.control.*': {'queue': 'control'},
        'app.tasks.maintenance.*': {'queue': 'maintenance'},
    },
)

# Define queues
celery_app.conf.task_queues = (
    Queue('workflows', Exchange('workflows'), routing_key='workflows'),
    Queue('control', Exchange('control'), routing_key='control'),
    Queue('maintenance', Exchange('maintenance'), routing_key='maintenance'),
)

# Beat schedule (periodic tasks)
celery_app.conf.beat_schedule = {
    'self-protect-cycle': {
        'task': 'app.tasks.control.self_protect_cycle_with_safety',
        'schedule': schedule(run_every=30),
    },
    'rapid-stuck-detection': {
        'task': 'app.tasks.maintenance.rapid_stuck_task_detection',
        'schedule': schedule(run_every=5),
    },
    'verify-stability': {
        'task': 'app.tasks.maintenance.verify_system_stability',
        'schedule': schedule(run_every=300),
    },
    'retry-pending-next-stages': {
        'task': 'app.tasks.maintenance.retry_pending_next_stages',
        'schedule': schedule(run_every=60),
    },
}

logger.info(f"Celery configured: soft_timeout={settings.CELERY_TASK_SOFT_TIME_LIMIT}s, "
           f"hard_timeout={settings.CELERY_TASK_TIME_LIMIT}s")
