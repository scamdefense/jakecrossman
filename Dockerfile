# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install all dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run code quality checks and tests
RUN black --check .
RUN flake8 .
RUN pytest

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (using app.py as entry point)
COPY app/ ./app/
COPY app.py .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]