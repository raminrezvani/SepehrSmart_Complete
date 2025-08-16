import environ
import os

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env('.env')

APP_PORT = env('APP_PORT')

# Get the APP_PORT from environment variable or set a default
bind = f"0.0.0.0:{os.environ.get('APP_PORT', 5000)}"
workers = 3  # Adjust the number of workers as needed
