"""Dashboard definitions for system observability."""
from typing import List, Dict, Any


class DashboardPanel:
    """Represents a single dashboard panel."""

    def __init__(
        self,
        title: str,
        metric: str,
        panel_type: str = "graph",  # graph, stat, table, gauge
        unit: str = "",
        thresholds: List[float] = None,
    ):
        self.title = title
        self.metric = metric
        self.panel_type = panel_type
        self.unit = unit
        self.thresholds = thresholds or []

    def to_dict(self) -> dict:
        """Export panel as dictionary."""
        return {
            "title": self.title,
            "metric": self.metric,
            "type": self.panel_type,
            "unit": self.unit,
            "thresholds": self.thresholds,
        }


class Dashboard:
    """Represents a Grafana-style dashboard."""

    def __init__(self, name: str, description: str, tags: List[str] = None):
        self.name = name
        self.description = description
        self.tags = tags or []
        self.panels: List[DashboardPanel] = []

    def add_panel(self, panel: DashboardPanel):
        """Add a panel to the dashboard."""
        self.panels.append(panel)

    def to_dict(self) -> dict:
        """Export dashboard as dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "panels": [p.to_dict() for p in self.panels],
        }


class SystemDashboards:
    """Pre-defined dashboards for the system."""

    @staticmethod
    def system_health_dashboard() -> Dashboard:
        """Dashboard for overall system health."""
        dashboard = Dashboard(
            name="System Health",
            description="Overall system health and status",
            tags=["system", "health"],
        )

        dashboard.add_panel(DashboardPanel(
            title="API Request Rate",
            metric="rate(api_requests_total[5m])",
            panel_type="graph",
            unit="req/s",
        ))

        dashboard.add_panel(DashboardPanel(
            title="Error Rate",
            metric="rate(api_errors_total[5m]) / rate(api_requests_total[5m])",
            panel_type="gauge",
            unit="percent",
            thresholds=[0.01, 0.05],
        ))

        dashboard.add_panel(DashboardPanel(
            title="P99 Latency",
            metric="histogram_quantile(0.99, api_request_latency_ms)",
            panel_type="graph",
            unit="ms",
        ))

        dashboard.add_panel(DashboardPanel(
            title="Database Connections",
            metric="db_connections_active",
            panel_type="stat",
            unit="connections",
        ))

        return dashboard

    @staticmethod
    def event_flow_dashboard() -> Dashboard:
        """Dashboard for event system monitoring."""
        dashboard = Dashboard(
            name="Event Flow",
            description="Event publishing and consumption metrics",
            tags=["events", "system"],
        )

        dashboard.add_panel(DashboardPanel(
            title="Events Published",
            metric="rate(events_published_total[5m])",
            panel_type="graph",
            unit="events/s",
        ))

        dashboard.add_panel(DashboardPanel(
            title="Event Publish Latency",
            metric="histogram_quantile(0.95, event_publish_latency_ms)",
            panel_type="graph",
            unit="ms",
        ))

        dashboard.add_panel(DashboardPanel(
            title="Consumer Lag",
            metric="consumer_lag",
            panel_type="graph",
            unit="events",
            thresholds=[100, 1000],
        ))

        dashboard.add_panel(DashboardPanel(
            title="DLQ Size",
            metric="dlq_size",
            panel_type="stat",
            unit="events",
        ))

        return dashboard

    @staticmethod
    def execution_pipeline_dashboard() -> Dashboard:
        """Dashboard for execution pipeline monitoring."""
        dashboard = Dashboard(
            name="Execution Pipeline",
            description="Decision execution lifecycle and metrics",
            tags=["execution", "decisions"],
        )

        dashboard.add_panel(DashboardPanel(
            title="In Progress Executions",
            metric="executions_in_progress",
            panel_type="stat",
            unit="executions",
        ))

        dashboard.add_panel(DashboardPanel(
            title="Blocked Executions",
            metric="executions_blocked",
            panel_type="stat",
            unit="executions",
        ))

        dashboard.add_panel(DashboardPanel(
            title="Stale Executions",
            metric="executions_stale",
            panel_type="gauge",
            unit="executions",
            thresholds=[1, 10],
        ))

        dashboard.add_panel(DashboardPanel(
            title="Execution Duration",
            metric="histogram_quantile(0.95, execution_duration_ms)",
            panel_type="graph",
            unit="ms",
        ))

        return dashboard

    @staticmethod
    def cost_monitoring_dashboard() -> Dashboard:
        """Dashboard for cost monitoring."""
        dashboard = Dashboard(
            name="Cost Monitoring",
            description="Track system costs and spending",
            tags=["cost", "billing"],
        )

        dashboard.add_panel(DashboardPanel(
            title="Tokens Used Rate",
            metric="rate(tokens_used_total[1h])",
            panel_type="graph",
            unit="tokens/hour",
        ))

        dashboard.add_panel(DashboardPanel(
            title="Cost per Decision",
            metric="cost_per_decision",
            panel_type="gauge",
            unit="$",
            thresholds=[1.0, 5.0],
        ))

        dashboard.add_panel(DashboardPanel(
            title="Cost per Execution",
            metric="cost_per_execution",
            panel_type="gauge",
            unit="$",
            thresholds=[0.5, 2.0],
        ))

        dashboard.add_panel(DashboardPanel(
            title="Daily Spend Estimate",
            metric="rate(tokens_used_total[1h]) * 24 / 1000000",  # Rough estimate
            panel_type="stat",
            unit="$",
        ))

        return dashboard

    @staticmethod
    def decision_accuracy_dashboard() -> Dashboard:
        """Dashboard for decision accuracy tracking."""
        dashboard = Dashboard(
            name="Decision Accuracy",
            description="Track decision accuracy metrics and trends",
            tags=["decisions", "accuracy"],
        )

        dashboard.add_panel(DashboardPanel(
            title="Decisions Created",
            metric="rate(decisions_created_total[1d])",
            panel_type="graph",
            unit="decisions/day",
        ))

        dashboard.add_panel(DashboardPanel(
            title="Average Confidence",
            metric="decision_confidence_avg",
            panel_type="gauge",
            unit="percent",
            thresholds=[50, 75],
        ))

        dashboard.add_panel(DashboardPanel(
            title="Accuracy by Outcome",
            metric="decision_accuracy",
            panel_type="table",
            unit="percent",
        ))

        return dashboard

    @staticmethod
    def get_all_dashboards() -> List[Dashboard]:
        """Get all pre-defined dashboards."""
        return [
            SystemDashboards.system_health_dashboard(),
            SystemDashboards.event_flow_dashboard(),
            SystemDashboards.execution_pipeline_dashboard(),
            SystemDashboards.cost_monitoring_dashboard(),
            SystemDashboards.decision_accuracy_dashboard(),
        ]

    @staticmethod
    def export_all_dashboards() -> Dict[str, dict]:
        """Export all dashboards as dictionary."""
        dashboards = {}
        for dashboard in SystemDashboards.get_all_dashboards():
            dashboards[dashboard.name] = dashboard.to_dict()
        return dashboards
