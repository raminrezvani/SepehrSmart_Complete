# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5002

# Command to run the application
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD sh -c "gunicorn -c /app/gunicorn_config.py deltaban_service:app --threads 4 --timeout 120 --access-logfile - --access-logformat '%(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %(M)s'"
