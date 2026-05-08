# Use Python slim image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
