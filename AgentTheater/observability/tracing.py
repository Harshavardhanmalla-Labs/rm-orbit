"""Distributed tracing setup using OpenTelemetry."""
from typing import Optional
from uuid import uuid4


class TraceContext:
    """Manages trace context propagation."""

    def __init__(self, trace_id: Optional[str] = None, parent_span_id: Optional[str] = None):
        self.trace_id = trace_id or str(uuid4())
        self.parent_span_id = parent_span_id
        self.span_stack = []

    def start_span(self, name: str, attributes: dict = None) -> "Span":
        """Start a new span in this trace."""
        span = Span(
            trace_id=self.trace_id,
            span_id=str(uuid4()),
            parent_span_id=self.parent_span_id or (self.span_stack[-1].span_id if self.span_stack else None),
            name=name,
            attributes=attributes or {},
        )
        self.span_stack.append(span)
        return span

    def end_span(self, span: "Span"):
        """End a span and pop it from the stack."""
        if self.span_stack and self.span_stack[-1].span_id == span.span_id:
            self.span_stack.pop()
        span.end()


class Span:
    """Represents a single span in a distributed trace."""

    def __init__(
        self,
        trace_id: str,
        span_id: str,
        parent_span_id: Optional[str],
        name: str,
        attributes: dict = None,
    ):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_span_id = parent_span_id
        self.name = name
        self.attributes = attributes or {}
        self.start_time = None
        self.end_time = None

    def add_attribute(self, key: str, value):
        """Add an attribute to this span."""
        self.attributes[key] = value

    def add_event(self, name: str, attributes: dict = None):
        """Record an event within this span."""
        if "events" not in self.attributes:
            self.attributes["events"] = []
        self.attributes["events"].append({
            "name": name,
            "attributes": attributes or {},
        })

    def end(self):
        """Mark span as ended."""
        pass

    def to_dict(self) -> dict:
        """Export span as dictionary."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "name": self.name,
            "attributes": self.attributes,
        }


class TracingMiddleware:
    """Middleware to attach tracing context to requests."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        """ASGI middleware for tracing."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Extract or create trace context
        headers = dict(scope.get("headers", []))
        correlation_id = headers.get(b"x-correlation-id", b"").decode()
        trace_id = headers.get(b"x-trace-id", b"").decode() or correlation_id or str(uuid4())

        # Store in scope for handlers to access
        scope["trace_id"] = trace_id
        scope["correlation_id"] = correlation_id

        async def send_with_headers(message):
            """Add trace headers to response."""
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append((b"x-trace-id", trace_id.encode()))
                if correlation_id:
                    headers.append((b"x-correlation-id", correlation_id.encode()))
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_headers)


def create_trace_context(correlation_id: Optional[str] = None) -> TraceContext:
    """Create a new trace context from correlation_id."""
    return TraceContext(trace_id=correlation_id or str(uuid4()))
