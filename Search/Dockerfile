FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY scripts ./scripts

# Search needs access to Learn site docs
# These should be provided via a volume or copied from a builder
# In production, we assume Learn is a separate service, 
# but Search needs the HTML files to index them.
# We'll copy them for now or use a shared volume.
COPY Learn/site ./Learn/site

ENV SEARCH_LEARN_SITE_DIR=/app/Learn/site
ENV SEARCH_WRITER_API_BASE=http://writer-backend:6011
ENV PORT=6200

EXPOSE 6200

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6200"]
