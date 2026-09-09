# System Health Dashboard API - Docker image
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py .

# Default environment (overridable at "docker run" time with -e APP_ENV=...)
ENV APP_ENV=production
EXPOSE 5000

# Run with gunicorn instead of the Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]