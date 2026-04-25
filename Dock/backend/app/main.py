from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import router as persistent_router

app = FastAPI(title="RM Dock API", version="0.2.0")

# Primary Dock API surface is now database-backed.
app.include_router(persistent_router, prefix="/api/dock", tags=["dock"])
# Compatibility alias while clients are migrated.
app.include_router(persistent_router, prefix="/api/dock/persistent", tags=["persistent"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"service": "rm-dock", "status": "ok"}


DIST_PATH = Path(__file__).resolve().parents[1] / "frontend" / "dist"
if not DIST_PATH.exists():
    DIST_PATH = Path(__file__).resolve().parents[2] / "frontend" / "dist"

if DIST_PATH.exists():
    assets_dir = DIST_PATH / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="dock-assets")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi"):
            return None

        target = DIST_PATH / full_path
        if target.is_file():
            return FileResponse(target)

        return FileResponse(DIST_PATH / "index.html")
