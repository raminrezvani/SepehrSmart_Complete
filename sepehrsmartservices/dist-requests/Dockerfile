# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    REQUEST_LINE_LIMIT=32768

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        psmisc \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the ports the app listens on
EXPOSE 6000 6001 6002 6003 6004 6005

# Ensure logs directory exists
RUN mkdir -p /app/logs

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

# Default command: run the main script
# CMD sh -c "python3 Server_Distribute_req_Call_ALL_LINUX.py"
# CMD ["gunicorn", "-w", "3", "--threads", "4", "--access-logfile", "-", "-b", "0.0.0.0:6000", "-b", "0.0.0.0:6001", "-b", "0.0.0.0:6002", "-b", "0.0.0.0:6003", "-b", "0.0.0.0:6004", "-b", "0.0.0.0:6005", "--limit-request-line", "32768", "Server_Distribute_req:app"]
