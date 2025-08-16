# Use official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=hotel_providers_api.settings

# Set working directory
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

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port Django runs on
EXPOSE 8000

# Run Django application
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hotel_providers_api.wsgi:application"]

# Run migrations, then start Django application using gunicorn
CMD sh -c "python manage.py migrate auth && python manage.py migrate --run-syncdb && gunicorn --bind 0.0.0.0:8000 hotel_providers_api.wsgi:application --timeout 180 --workers 1 --threads 8 --access-logfile - --access-logformat '%(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %(T)s' "
