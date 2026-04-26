"""AgentTheatre FastAPI Application with Systems 1-7."""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from AgentTheater.events.db_models import Base
from AgentTheater.events.outbox_relay import run_outbox_relay
from AgentTheater.observability import (
    setup_structured_logging,
    get_metrics,
    HealthChecker,
    AlertRules,
    SystemDashboards,
)
from AgentTheater.api.middleware import ObservabilityMiddleware

# Configure structured JSON logging at startup
setup_structured_logging(log_level="INFO")

try:
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

try:
    from AgentTheater.observability import TracingMiddleware
    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False

# Database setup (must come before lifespan so engine is in scope)
DATABASE_URL = "sqlite+aiosqlite:///./agenttheatre.db"
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup; run outbox relay; clean up on shutdown."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    relay_task = asyncio.create_task(
        run_outbox_relay(AsyncSessionLocal, interval_seconds=5.0),
        name="outbox-relay",
    )

    yield

    relay_task.cancel()
    try:
        await relay_task
    except asyncio.CancelledError:
        pass
    await engine.dispose()


app = FastAPI(
    title="AgentTheatre",
    description="Decision intelligence platform with event sourcing",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(ObservabilityMiddleware)

# allow_credentials=True is incompatible with allow_origins=["*"] (browsers reject it).
# Scope origins explicitly; extend this list per deployment environment.
_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:45018",
    "https://*.freedomlabs.in",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_db() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_event_store():
    """Get event store."""
    from AgentTheater.events import EventStore
    async with AsyncSessionLocal() as session:
        yield EventStore(session)


# Import routers to set up dependency overrides
from AgentTheater.api.versions.v1 import decisions_router as dr
from AgentTheater.api.versions.v1 import accountability_router as ar
from AgentTheater.api.versions.v1 import execution_router as exr

app.dependency_overrides[dr.get_db] = get_db
app.dependency_overrides[dr.get_event_store] = get_event_store
app.dependency_overrides[ar.get_db] = get_db
app.dependency_overrides[ar.get_event_store] = get_event_store
app.dependency_overrides[exr.get_db] = get_db
app.dependency_overrides[exr.get_event_store] = get_event_store

# Register routes
app.include_router(dr.router, prefix="/api/v1", tags=["decisions"])
app.include_router(ar.router, prefix="/api/v1", tags=["accountability"])
app.include_router(exr.router, prefix="/api/v1", tags=["execution"])


@app.get("/health/live")
async def liveness():
    """Kubernetes liveness probe — just checks process is alive."""
    return {"alive": True}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/health/deep")
async def deep_health(db: AsyncSession = Depends(get_db)):
    checker = HealthChecker(db)
    return await checker.deep_health()


@app.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    checker = HealthChecker(db)
    return await checker.readiness()


@app.get("/metrics")
async def metrics():
    if not PROMETHEUS_AVAILABLE:
        return JSONResponse({"error": "Prometheus client not installed"}, status_code=503)
    metrics_instance = get_metrics()
    return JSONResponse(
        content=generate_latest(metrics_instance.registry).decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/observability/alerts")
async def get_alerts():
    return {"alerts": AlertRules.to_dict()}


@app.get("/observability/dashboards")
async def get_dashboards():
    return SystemDashboards.export_all_dashboards()


@app.get("/observability/config")
async def observability_config():
    return {
        "logging": "structured_json",
        "metrics": "prometheus",
        "tracing": "opentelemetry",
        "alerts": len(AlertRules.RULES),
        "dashboards": len(SystemDashboards.get_all_dashboards()),
    }
