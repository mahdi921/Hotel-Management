# Base image: Python Alpine for minimal size
FROM python:alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies required for psycopg[binary] and other packages
RUN apk add --no-cache \
    # PostgreSQL client libraries
    postgresql-dev \
    # Build dependencies (needed for some Python packages)
    gcc \
    musl-dev \
    python3-dev \
    # For Pillow (image processing)
    jpeg-dev \
    zlib-dev \
    libjpeg \
    # For cryptography
    libffi-dev \
    openssl-dev \
    # For translations
    gettext

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port for Django/FastAPI
EXPOSE 8000

# Default command (can be overridden in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
