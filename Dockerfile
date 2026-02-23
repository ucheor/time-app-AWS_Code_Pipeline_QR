# ─────────────────────────────────────────────────────────
#  Time Zones - North America  ·  Python / Flask  ·  Docker Image
#  HTML frontend  +  Python backend API  ·  Port 5000
# ─────────────────────────────────────────────────────────
FROM python:3.12-slim

LABEL description="Time Zones - North America – Flask backend + HTML frontend"
LABEL version="2.1"

# Create non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY index.html .

# Switch to non-root user
USER appuser

EXPOSE 5000

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]