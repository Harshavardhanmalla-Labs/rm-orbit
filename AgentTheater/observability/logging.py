"""Structured JSON logging for production observability."""
import logging
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID

try:
    from pythonjsonlogger import jsonlogger
    HAS_JSON_LOGGER = True
except ImportError:
    HAS_JSON_LOGGER = False

    # Fallback formatter if pythonjsonlogger not installed
    class JsonFormatter(logging.Formatter):
        """Simple JSON formatter fallback."""
        def format(self, record):
            log_dict = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
            return json.dumps(log_dict)

    class jsonlogger:
        JsonFormatter = JsonFormatter


class StructuredFormatter(jsonlogger.JsonFormatter):
    """JSON formatter with structured context fields."""

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]):
        """Add standard fields to all log entries."""
        super().add_fields(log_record, record, message_dict)

        # Add timestamp in ISO format
        log_record["timestamp"] = datetime.now(timezone.utc).isoformat()

        # Add level
        log_record["level"] = record.levelname

        # Add logger name
        log_record["logger"] = record.name

        # Add context from LoggerAdapter if available
        if hasattr(record, "request_id") and record.request_id:
            log_record["request_id"] = record.request_id
        if hasattr(record, "correlation_id") and record.correlation_id:
            log_record["correlation_id"] = record.correlation_id
        if hasattr(record, "tenant_id") and record.tenant_id:
            log_record["tenant_id"] = str(record.tenant_id)
        if hasattr(record, "user_id") and record.user_id:
            log_record["user_id"] = str(record.user_id)
        if hasattr(record, "event_id") and record.event_id:
            log_record["event_id"] = str(record.event_id)
        if hasattr(record, "trace_id") and record.trace_id:
            log_record["trace_id"] = record.trace_id

        # Add execution context if available
        if hasattr(record, "latency_ms") and record.latency_ms:
            log_record["latency_ms"] = record.latency_ms
        if hasattr(record, "status_code") and record.status_code:
            log_record["status_code"] = record.status_code
        if hasattr(record, "endpoint") and record.endpoint:
            log_record["endpoint"] = record.endpoint


class ContextualLogger:
    """Logger with attached context (request_id, correlation_id, etc.)."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.context = {}

    def set_context(
        self,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        tenant_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        trace_id: Optional[str] = None,
    ):
        """Set context fields that will be included in all log messages."""
        if request_id:
            self.context["request_id"] = request_id
        if correlation_id:
            self.context["correlation_id"] = correlation_id
        if tenant_id:
            self.context["tenant_id"] = str(tenant_id)
        if user_id:
            self.context["user_id"] = str(user_id)
        if trace_id:
            self.context["trace_id"] = trace_id

    def add_context(self, **kwargs):
        """Add additional context fields."""
        self.context.update(kwargs)

    def _log(self, level: int, msg: str, extra: Dict[str, Any] = None):
        """Log with context."""
        log_extra = {**self.context, **(extra or {})}
        # Set attributes on the record via LoggerAdapter
        adapter = logging.LoggerAdapter(self.logger, log_extra)
        adapter.log(level, msg)

    def debug(self, msg: str, **kwargs):
        """Log debug message."""
        self._log(logging.DEBUG, msg, kwargs)

    def info(self, msg: str, **kwargs):
        """Log info message."""
        self._log(logging.INFO, msg, kwargs)

    def warning(self, msg: str, **kwargs):
        """Log warning message."""
        self._log(logging.WARNING, msg, kwargs)

    def error(self, msg: str, **kwargs):
        """Log error message."""
        self._log(logging.ERROR, msg, kwargs)

    def critical(self, msg: str, **kwargs):
        """Log critical message."""
        self._log(logging.CRITICAL, msg, kwargs)


def setup_structured_logging(log_level: str = "INFO"):
    """Set up structured JSON logging for the application."""
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler with JSON formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(console_handler)

    return root_logger
