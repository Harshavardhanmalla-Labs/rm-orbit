"""Alert rules for production observability."""
from typing import List, Dict, Any
from enum import Enum


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class AlertRule:
    """Represents an alert rule for monitoring."""

    def __init__(
        self,
        name: str,
        description: str,
        metric: str,
        threshold: float,
        duration_seconds: int,
        severity: AlertSeverity,
        condition: str = ">",  # ">" or "<"
        annotations: Dict[str, str] = None,
    ):
        self.name = name
        self.description = description
        self.metric = metric
        self.threshold = threshold
        self.duration_seconds = duration_seconds
        self.severity = severity
        self.condition = condition
        self.annotations = annotations or {}

    def to_prometheus_rule(self) -> str:
        """Export as Prometheus alert rule."""
        return f"""
- alert: {self.name}
  expr: {self.metric} {self.condition} {self.threshold}
  for: {self.duration_seconds}s
  annotations:
    summary: "{self.description}"
    severity: "{self.severity.value}"
"""

    def to_dict(self) -> dict:
        """Export as dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "metric": self.metric,
            "threshold": self.threshold,
            "duration_seconds": self.duration_seconds,
            "severity": self.severity.value,
            "condition": self.condition,
            "annotations": self.annotations,
        }


class AlertRules:
    """Collection of alert rules for the system."""

    RULES: List[AlertRule] = [
        # API Layer Alerts
        AlertRule(
            name="HighErrorRate",
            description="API error rate > 5%",
            metric="rate(api_errors_total[5m]) / rate(api_requests_total[5m])",
            threshold=0.05,
            duration_seconds=300,
            severity=AlertSeverity.CRITICAL,
            condition=">",
        ),
        AlertRule(
            name="HighLatency",
            description="API P99 latency > 2000ms",
            metric="histogram_quantile(0.99, api_request_latency_ms)",
            threshold=2000,
            duration_seconds=600,
            severity=AlertSeverity.WARNING,
            condition=">",
        ),

        # Event System Alerts
        AlertRule(
            name="HighEventLag",
            description="Consumer lag > 1000 events",
            metric="consumer_lag",
            threshold=1000,
            duration_seconds=300,
            severity=AlertSeverity.WARNING,
            condition=">",
        ),
        AlertRule(
            name="DLQGrowth",
            description="Dead letter queue size > 100",
            metric="dlq_size",
            threshold=100,
            duration_seconds=600,
            severity=AlertSeverity.CRITICAL,
            condition=">",
        ),

        # Execution System Alerts
        AlertRule(
            name="StaleExecutions",
            description="Stale executions (>7 days) > 10",
            metric="executions_stale",
            threshold=10,
            duration_seconds=1800,
            severity=AlertSeverity.WARNING,
            condition=">",
        ),
        AlertRule(
            name="TooManyBlocked",
            description="Blocked executions > 50",
            metric="executions_blocked",
            threshold=50,
            duration_seconds=600,
            severity=AlertSeverity.WARNING,
            condition=">",
        ),

        # Cost Alerts
        AlertRule(
            name="CostSpike",
            description="Cost per decision > threshold",
            metric="cost_per_decision",
            threshold=5.0,  # $5 per decision
            duration_seconds=900,
            severity=AlertSeverity.WARNING,
            condition=">",
        ),
        AlertRule(
            name="HighTokenUsage",
            description="Tokens used > 1M in 5 minutes",
            metric="rate(tokens_used_total[5m])",
            threshold=1000000,
            duration_seconds=300,
            severity=AlertSeverity.INFO,
            condition=">",
        ),

        # Database Alerts
        AlertRule(
            name="SlowQueries",
            description="Database P99 latency > 500ms",
            metric="histogram_quantile(0.99, db_query_latency_ms)",
            threshold=500,
            duration_seconds=600,
            severity=AlertSeverity.WARNING,
            condition=">",
        ),
    ]

    @classmethod
    def get_all_rules(cls) -> List[AlertRule]:
        """Get all alert rules."""
        return cls.RULES

    @classmethod
    def to_prometheus_rules(cls) -> str:
        """Export all rules as Prometheus alert rules."""
        rules_text = "groups:\n- name: agenttheatre_alerts\n  rules:\n"
        for rule in cls.RULES:
            rules_text += rule.to_prometheus_rule()
        return rules_text

    @classmethod
    def to_dict(cls) -> List[dict]:
        """Export all rules as dictionaries."""
        return [rule.to_dict() for rule in cls.RULES]
