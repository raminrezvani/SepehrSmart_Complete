# Use the official Python image from the Docker Hub
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

# Expose the port the app runs on
EXPOSE 5003

# Command to run the application
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD sh -c "gunicorn -c /app/gunicorn_config.py Crawl_alaedin_Rooms_Flask_OK:app --threads 6 --timeout 120 --access-logfile - --access-logformat '%(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %(M)s'"
