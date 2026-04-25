from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api.papers import router as papers_router
from app.api.intake import router as intake_router
from app.api.pipeline_router import router as pipeline_router
from app.api.export_router import router as export_router
from app.api.system import router as system_router
from app.middleware import RequestContextMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Research Platform API",
    description="Autonomous AI-powered research paper writing — RM Orbit",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestContextMiddleware)

app.include_router(papers_router)
app.include_router(intake_router)
app.include_router(pipeline_router)
app.include_router(export_router)
app.include_router(system_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "research-api", "port": 6420}


@app.get("/")
async def root():
    return {"service": "Research Platform", "docs": "/docs", "health": "/health"}
