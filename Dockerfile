# Production Dockerfile for CampusEnroll
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency definition
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Initialize database schema & seed data
RUN python database/init_db.py

# Expose port 5000
EXPOSE 5000

# Set production environment variables
ENV PORT=5000
ENV FLASK_DEBUG=False

# Run using Gunicorn (or wsgi.py)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "wsgi:app"]
