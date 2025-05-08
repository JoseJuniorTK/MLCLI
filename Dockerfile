FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Convert line endings to LF for entrypoint (Windows safety)
RUN dos2unix /usr/local/bin/entrypoint.sh || true

# Set Python path
ENV PYTHONPATH=/app

# Create necessary directories
RUN mkdir -p models metrics data output

# Copy and fix permissions for entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN dos2unix /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh

# Add a non-root user
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -u ${USER_ID} -g appuser -s /bin/bash -m appuser && \
    chown -R appuser:appuser /app

# Fix ownership for output directory
RUN chown -R appuser:appuser /app/output

USER appuser

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
