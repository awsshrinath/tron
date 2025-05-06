# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all source code into the image
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to force unbuffered logs
ENV PYTHONUNBUFFERED=1

# Default command (can be overridden by deployment YAML or docker-compose)
CMD ["python", "main_runner.py"]
