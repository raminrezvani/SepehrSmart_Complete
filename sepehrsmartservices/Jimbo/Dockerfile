# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libxss1 \
    libappindicator3-1 \
    fonts-liberation \
    libgtk-3-0 \
    && apt-get clean

# Install Google Chrome
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_135.0.7049.52-1_amd64.deb && \
    apt-get install -y ./google-chrome-stable_135.0.7049.52-1_amd64.deb && \
    rm google-chrome-stable_135.0.7049.52-1_amd64.deb

# Install ChromeDriver (static version)
RUN wget "https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.52/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver-linux64.zip

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the ports the apps run on
EXPOSE 3030 5021

# Run supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
