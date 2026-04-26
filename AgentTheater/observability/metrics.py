"""Prometheus metrics instrumentation for production observability."""
try:
    from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
except ImportError:
    # Fallback mock classes if prometheus_client not installed
    class Counter:
        def __init__(self, *args, **kwargs): pass
        def labels(self, *args, **kwargs): return self
        def inc(self, *args, **kwargs): pass

    class Histogram:
        def __init__(self, *args, **kwargs): pass
        def labels(self, *args, **kwargs): return self
        def observe(self, *args, **kwargs): pass

    class Gauge:
        def __init__(self, *args, **kwargs): pass
        def labels(self, *args, **kwargs): return self
        def set(self, *args, **kwargs): pass
        def inc(self, *args, **kwargs): pass
        def dec(self, *args, **kwargs): pass

    class CollectorRegistry:
        pass


class AgentTheatreMetrics:
    """Central registry for all application metrics."""

    def __init__(self, registry: CollectorRegistry = None):
        self.registry = registry or CollectorRegistry()

        # API Layer Metrics
        self.api_requests_total = Counter(
            "api_requests_total",
            "Total API requests",
            ["method", "endpoint", "status", "version"],
            registry=self.registry,
        )

        self.api_request_latency_ms = Histogram(
            "api_request_latency_ms",
            "API request latency in milliseconds",
            ["method", "endpoint", "version"],
            buckets=(10, 50, 100, 250, 500, 1000, 2500, 5000),
            registry=self.registry,
        )

        self.api_errors_total = Counter(
            "api_errors_total",
            "Total API errors",
            ["endpoint", "error_type", "status"],
            registry=self.registry,
        )

        # Event System Metrics
        self.events_published_total = Counter(
            "events_published_total",
            "Total events published",
            ["event_type", "aggregate_type"],
            registry=self.registry,
        )

        self.event_publish_latency_ms = Histogram(
            "event_publish_latency_ms",
            "Event publish latency in milliseconds",
            ["event_type"],
            buckets=(1, 5, 10, 25, 50, 100, 250, 500),
            registry=self.registry,
        )

        self.dlq_size = Gauge(
            "dlq_size",
            "Number of events in dead letter queue",
            ["event_type"],
            registry=self.registry,
        )

        self.consumer_lag = Gauge(
            "consumer_lag",
            "Consumer lag in events",
            ["consumer_name"],
            registry=self.registry,
        )

        # Execution System Metrics
        self.executions_in_progress = Gauge(
            "executions_in_progress",
            "Number of executions in progress",
            ["tenant_id"],
            registry=self.registry,
        )

        self.executions_blocked = Gauge(
            "executions_blocked",
            "Number of blocked executions",
            ["tenant_id", "blocked_reason"],
            registry=self.registry,
        )

        self.executions_stale = Gauge(
            "executions_stale",
            "Number of stale executions (in_progress > threshold)",
            ["tenant_id"],
            registry=self.registry,
        )

        self.execution_duration_ms = Histogram(
            "execution_duration_ms",
            "Execution duration in milliseconds",
            ["outcome"],
            buckets=(1000, 5000, 10000, 30000, 60000, 300000, 3600000),
            registry=self.registry,
        )

        # Decision System Metrics
        self.decisions_created_total = Counter(
            "decisions_created_total",
            "Total decisions created",
            ["tenant_id"],
            registry=self.registry,
        )

        self.decision_confidence_avg = Gauge(
            "decision_confidence_avg",
            "Average decision confidence score",
            ["tenant_id"],
            registry=self.registry,
        )

        self.decision_accuracy = Gauge(
            "decision_accuracy",
            "Decision accuracy (predicted vs actual outcome match rate)",
            ["tenant_id", "outcome_type"],
            registry=self.registry,
        )

        # Cost Tracking Metrics
        self.tokens_used_total = Counter(
            "tokens_used_total",
            "Total LLM tokens used",
            ["request_type", "model"],
            registry=self.registry,
        )

        self.cost_per_decision = Gauge(
            "cost_per_decision",
            "Average cost per decision",
            ["tenant_id"],
            registry=self.registry,
        )

        self.cost_per_execution = Gauge(
            "cost_per_execution",
            "Average cost per execution",
            ["tenant_id"],
            registry=self.registry,
        )

        # Database Metrics
        self.db_query_latency_ms = Histogram(
            "db_query_latency_ms",
            "Database query latency in milliseconds",
            ["query_type", "table"],
            buckets=(1, 5, 10, 25, 50, 100, 250),
            registry=self.registry,
        )

        self.db_connections_active = Gauge(
            "db_connections_active",
            "Number of active database connections",
            registry=self.registry,
        )

        # Outbox & Relay Metrics
        self.outbox_unpublished_count = Gauge(
            "outbox_unpublished_count",
            "Current number of unpublished events in the outbox",
            registry=self.registry,
        )

        self.outbox_publish_failures_total = Counter(
            "outbox_publish_failures_total",
            "Total outbox publish delivery failures",
            ["event_type"],
            registry=self.registry,
        )

        # Guardrail Metrics
        self.guardrail_blocks_total = Counter(
            "guardrail_blocks_total",
            "Total guardrail blocks triggered",
            ["tenant_id", "guardrail_name"],
            registry=self.registry,
        )

        # Event Reliability
        self.event_commit_failures_total = Counter(
            "event_commit_failures_total",
            "Total transactional event commit failures",
            ["event_type"],
            registry=self.registry,
        )


# Global metrics instance
_metrics_instance = None


def get_metrics(registry: CollectorRegistry = None) -> AgentTheatreMetrics:
    """Get or create global metrics instance."""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = AgentTheatreMetrics(registry)
    return _metrics_instance


def reset_metrics():
    """Reset global metrics instance (for testing)."""
    global _metrics_instance
    _metrics_instance = None
