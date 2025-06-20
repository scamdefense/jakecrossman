# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install all dependencies including scraping libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run code quality checks and tests
RUN black --check .
RUN flake8 .
RUN pytest

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies including scraping libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (using wsgi.py as entry point)
COPY app/ ./app/
COPY wsgi.py .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
