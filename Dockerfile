# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by telethon and cryptg
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY public/ ./public/

# Create directory for session files
RUN mkdir -p /app/sessions

# Set environment variables (can be overridden at runtime)
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "public/bot.py"]