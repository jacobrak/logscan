# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    git \
    curl \
    && apt-get clean

# Copy requirement files
COPY requirements.txt .

# Install Python dependencies with constraint for airflow
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Default command (can be overwritten)
CMD ["python"]
