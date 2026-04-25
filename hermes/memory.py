"""
HermesMemory — persistent FTS5 memory for RM Orbit services.

Stores per-user, per-service context that persists across sessions.
Used by Mail (smart triage learns your preferences), Calendar (learns
meeting patterns), Connect (conversation context), Writer (writing style).

DB location: Configured via ORBIT_MEMORY_DB env var.
Default: ~/.orbit/hermes_memory.db (on the server that runs Orbit backends)
For multi-tenant: use per-tenant paths or prefix memories with tenant_id.
"""

import asyncio
import logging
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

MEMORY_DB = os.getenv(
    "ORBIT_MEMORY_DB",
    str(Path.home() / ".orbit" / "hermes_memory.db")
)


@dataclass
class Memory:
    id: int
    service: str
    user_id: str
    org_id: str
    content: str
    tags: list[str]
    timestamp: str


class HermesMemory:
    """
    Persistent FTS5 memory store shared across all RM Orbit services.

    Thread-safe via asyncio.to_thread. Safe to use in FastAPI async handlers.
    """

    def __init__(self, service: str, user_id: str = "", org_id: str = ""):
        self.service = service
        self.user_id = user_id
        self.org_id = org_id
        self._db = MEMORY_DB
        _ensure_db(self._db)

    async def save(self, content: str, tags: list[str] | None = None) -> None:
        """Store a memory entry."""
        tag_str = " ".join(tags or [])
        ts = datetime.now(timezone.utc).isoformat()
        await asyncio.to_thread(_save, self._db, self.service,
                                 self.user_id, self.org_id, content, tag_str, ts)

    async def search(self, query: str, limit: int = 10) -> list[Memory]:
        """Full-text search scoped to this service + user + org."""
        return await asyncio.to_thread(
            _search, self._db, query, self.service, self.user_id, self.org_id, limit
        )

    async def search_global(self, query: str, limit: int = 10) -> list[Memory]:
        """Full-text search across all services (admin use)."""
        return await asyncio.to_thread(_search_all, self._db, query, limit)


# ── DB helpers (sync, run via asyncio.to_thread) ──────────────────────────────

def _ensure_db(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS orbit_memories USING fts5(
                service,
                user_id,
                org_id,
                content,
                tags,
                timestamp UNINDEXED,
                tokenize = 'porter unicode61'
            )
        """)
        conn.commit()


def _save(db: str, service: str, user_id: str, org_id: str,
          content: str, tags: str, ts: str) -> None:
    with sqlite3.connect(db) as conn:
        conn.execute(
            "INSERT INTO orbit_memories(service,user_id,org_id,content,tags,timestamp) "
            "VALUES (?,?,?,?,?,?)",
            (service, user_id, org_id, content, tags, ts)
        )
        conn.commit()


def _search(db: str, query: str, service: str, user_id: str,
            org_id: str, limit: int) -> list[Memory]:
    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            """SELECT rowid, service, user_id, org_id, content, tags, timestamp
               FROM orbit_memories
               WHERE orbit_memories MATCH ?
                 AND service = ? AND user_id = ? AND org_id = ?
               ORDER BY rank LIMIT ?""",
            (query, service, user_id, org_id, limit)
        ).fetchall()
    return [Memory(id=r[0], service=r[1], user_id=r[2], org_id=r[3],
                   content=r[4], tags=r[5].split(), timestamp=r[6]) for r in rows]


def _search_all(db: str, query: str, limit: int) -> list[Memory]:
    with sqlite3.connect(db) as conn:
        rows = conn.execute(
            """SELECT rowid, service, user_id, org_id, content, tags, timestamp
               FROM orbit_memories WHERE orbit_memories MATCH ?
               ORDER BY rank LIMIT ?""",
            (query, limit)
        ).fetchall()
    return [Memory(id=r[0], service=r[1], user_id=r[2], org_id=r[3],
                   content=r[4], tags=r[5].split(), timestamp=r[6]) for r in rows]
