import aiosqlite
import json
import uuid
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "research.db"


async def get_db():
    return aiosqlite.connect(str(DB_PATH))


async def init_db():
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id TEXT PRIMARY KEY,
                title TEXT,
                topic TEXT NOT NULL,
                niche TEXT NOT NULL,
                paper_type TEXT NOT NULL,
                target_venue TEXT NOT NULL,
                custom_template_path TEXT,
                author_name TEXT NOT NULL,
                author_affiliation TEXT DEFAULT '',
                word_count_target INTEGER DEFAULT 8000,
                status TEXT DEFAULT 'intake',
                current_stage TEXT DEFAULT 'intake',
                stage_progress REAL DEFAULT 0.0,
                error_message TEXT,
                warnings TEXT DEFAULT '[]',
                knowledge_map TEXT DEFAULT '{}',
                contribution_anchor TEXT DEFAULT '{}',
                outline TEXT DEFAULT '{}',
                sections TEXT DEFAULT '{}',
                citations TEXT DEFAULT '[]',
                confidence_report TEXT DEFAULT '{}',
                latex_path TEXT,
                docx_path TEXT,
                pdf_path TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id TEXT PRIMARY KEY,
                paper_id TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                stored_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER DEFAULT 0,
                has_equations INTEGER DEFAULT 0,
                parsed_text TEXT DEFAULT '',
                extraction_method TEXT DEFAULT '',
                extracted_word_count INTEGER DEFAULT 0,
                parse_warnings TEXT DEFAULT '[]',
                grobid_xml TEXT DEFAULT '',
                nougat_markdown TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        """)
        await _ensure_column(db, "uploads", "extraction_method", "TEXT DEFAULT ''")
        await _ensure_column(db, "uploads", "extracted_word_count", "INTEGER DEFAULT 0")
        await _ensure_column(db, "uploads", "parse_warnings", "TEXT DEFAULT '[]'")
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id TEXT NOT NULL,
                run_id TEXT,
                stage TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT DEFAULT '{}',
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        """)
        await _ensure_column(db, "pipeline_logs", "run_id", "TEXT")
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                id TEXT PRIMARY KEY,
                paper_id TEXT NOT NULL,
                status TEXT NOT NULL,
                started_at TEXT DEFAULT (datetime('now')),
                completed_at TEXT,
                current_stage TEXT DEFAULT 'stage_0_gate',
                stage_progress REAL DEFAULT 0.0,
                error_message TEXT,
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        """)
        await db.execute("""
            INSERT OR IGNORE INTO pipeline_runs (
                id, paper_id, status, started_at, completed_at, current_stage, stage_progress, error_message
            )
            SELECT
                'legacy-' || id,
                id,
                status,
                created_at,
                CASE
                    WHEN status IN ('complete', 'failed', 'cancelled') THEN updated_at
                    ELSE NULL
                END,
                current_stage,
                stage_progress,
                error_message
            FROM papers
            WHERE NOT EXISTS (
                SELECT 1 FROM pipeline_runs WHERE pipeline_runs.paper_id = papers.id
            )
        """)
        await db.commit()


async def update_paper(paper_id: str, **fields):
    if not fields:
        return
    fields["updated_at"] = "datetime('now')"
    set_parts = []
    values = []
    for k, v in fields.items():
        if k == "updated_at":
            set_parts.append(f"{k} = datetime('now')")
        else:
            if isinstance(v, (dict, list)):
                v = json.dumps(v)
            set_parts.append(f"{k} = ?")
            values.append(v)
    values.append(paper_id)
    sql = f"UPDATE papers SET {', '.join(set_parts)} WHERE id = ?"
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(sql, values)
        await db.commit()


async def get_paper(paper_id: str) -> dict | None:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)) as cur:
            row = await cur.fetchone()
            if not row:
                return None
            d = dict(row)
            for field in ("warnings", "knowledge_map", "contribution_anchor", "outline", "sections", "citations", "confidence_report"):
                if d.get(field):
                    try:
                        d[field] = json.loads(d[field])
                    except Exception:
                        pass
            return d


async def _ensure_column(db, table: str, column: str, definition: str):
    async with db.execute(f"PRAGMA table_info({table})") as cur:
        columns = [row[1] for row in await cur.fetchall()]
    if column not in columns:
        await db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


async def log_pipeline(paper_id: str, stage: str, status: str, message: str, details: dict = None, run_id: str | None = None):
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(
            "INSERT INTO pipeline_logs (paper_id, run_id, stage, status, message, details) VALUES (?, ?, ?, ?, ?, ?)",
            (paper_id, run_id, stage, status, message, json.dumps(details or {}))
        )
        await db.commit()


async def create_pipeline_run(paper_id: str) -> str:
    run_id = str(uuid.uuid4())
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(
            "INSERT INTO pipeline_runs (id, paper_id, status) VALUES (?, ?, 'processing')",
            (run_id, paper_id),
        )
        await db.commit()
    return run_id


async def update_pipeline_run(run_id: str | None, **fields):
    if not run_id or not fields:
        return
    set_parts = []
    values = []
    for key, value in fields.items():
        if key == "completed_at" and value == "now":
            set_parts.append("completed_at = datetime('now')")
        else:
            set_parts.append(f"{key} = ?")
            values.append(value)
    values.append(run_id)
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(f"UPDATE pipeline_runs SET {', '.join(set_parts)} WHERE id = ?", values)
        await db.commit()


async def get_latest_pipeline_run(paper_id: str) -> dict | None:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM pipeline_runs WHERE paper_id = ? ORDER BY started_at DESC LIMIT 1",
            (paper_id,),
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def get_pipeline_runs(paper_id: str) -> list[dict]:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM pipeline_runs WHERE paper_id = ? ORDER BY started_at DESC",
            (paper_id,),
        ) as cur:
            rows = await cur.fetchall()
            return [dict(row) for row in rows]


async def get_pipeline_run(run_id: str) -> dict | None:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM pipeline_runs WHERE id = ?", (run_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def get_uploads(paper_id: str) -> list[dict]:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM uploads WHERE paper_id = ?", (paper_id,)) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]


async def get_logs(paper_id: str) -> list[dict]:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM pipeline_logs WHERE paper_id = ? ORDER BY created_at ASC", (paper_id,)
        ) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]


async def get_run_logs(run_id: str) -> list[dict]:
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM pipeline_logs WHERE run_id = ? ORDER BY created_at ASC", (run_id,)
        ) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]
