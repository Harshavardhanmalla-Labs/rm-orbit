FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY frontend ./frontend

ENV PORT=6120
EXPOSE 6120

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6120"]
