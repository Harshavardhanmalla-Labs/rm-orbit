FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy source
COPY backend ./backend
COPY frontend ./frontend

# Environment defaults
ENV DATABASE_URL=postgresql+psycopg://postgres:postgres_secret@orbit-postgres:5432/orbit_wallet
ENV PORT=6110
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend

EXPOSE 6110

WORKDIR /app/backend
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 6110"]
