"""AgentTheatre FastAPI Application with System 1 + System 2 Integration."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from AgentTheater.events.db_models import Base

# Create FastAPI app
app = FastAPI(
    title="AgentTheatre",
    description="Decision intelligence platform with event sourcing",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./agenttheatre.db"
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_event_store():
    """Get event store."""
    from AgentTheater.events import EventStore

    async with AsyncSessionLocal() as session:
        yield EventStore(session)


# Set up dependency overrides in routers
from AgentTheater.api.versions.v1 import decisions_router as dr

dr.router.dependency_overrides = {
    dr.get_db: get_db,
    dr.get_event_store: get_event_store,
}


@app.on_event("startup")
async def startup():
    """Create tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Import routers
from AgentTheater.api.versions.v1 import decisions_router

# Register routes
app.include_router(decisions_router.router, prefix="/api/v1", tags=["decisions"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
