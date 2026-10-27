# Dockerfile for Hotel Management System Flask Web Application
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies list and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application source code
COPY . /app/

# Create uploads directory structure
RUN mkdir -p /app/static/uploads/id_proofs \
    /app/static/uploads/rooms \
    /app/static/uploads/staff_photos

# Expose web application port
EXPOSE 5000

# Entrypoint command running Gunicorn WSGI HTTP Server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
