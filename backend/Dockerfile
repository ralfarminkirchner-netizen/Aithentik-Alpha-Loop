FROM python:3.11-slim

WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment defaults
ENV HARBOR_PORT=8000
ENV PYTHONUNBUFFERED=1

# Healthcheck uses the same API key as traffic
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/status -H "X-API-Key: ${AITHENTIK_API_KEY}" || exit 1

# Start Harbor with 2 workers for resilience
CMD sh -c "uvicorn harbor:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2"
