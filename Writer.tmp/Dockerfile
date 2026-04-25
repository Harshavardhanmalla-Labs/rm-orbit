# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /web
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
COPY site/ ./site_fallback
RUN (npm run build) || (mkdir -p dist && cp -r ./site_fallback/* dist/ && echo "Fallback to site successful")

# Stage 2: Final Image
FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY --from=frontend-builder /web/dist ./frontend/dist

ENV PORT=6011
EXPOSE 6011

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6011"]
